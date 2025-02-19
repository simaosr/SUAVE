## @ingroup Methods-Weights-Buildups-eVTOL
# converge_evtol_weight.py

# Created: Aug 2022, M. Clarke

#-------------------------------------------------------------------------------
# Imports
#------------------------------------------------------------------------------- 
from SUAVE.Methods.Weights.Buildups.eVTOL.empty import empty
from SUAVE.Core import Data

#-------------------------------------------------------------------------------
# Empty
#-------------------------------------------------------------------------------

## @ingroup Methods-Weights-Buildups-eVTOL 
def converge_evtol_weight(vehicle,
                          print_iterations = False):
    '''Converges the maximum takeoff weight of an aircraft using the eVTOL 
    weight buildup routine.  
    
    Source:
    None
    
    Assumptions:
    None
    
    Inputs:
    vehicle                     SUAVE Config Data Stucture
    print_iterations            Boolean Flag      
    contingency_factor          Factor capturing uncertainty in vehicle weight [Unitless]
    speed_of_sound:             Local Speed of Sound                           [m/s]
    max_tip_mach:               Allowable Tip Mach Number                      [Unitless]
    disk_area_factor:           Inverse of Disk Area Efficiency                [Unitless]
    max_thrust_to_weight_ratio: Allowable Thrust to Weight Ratio               [Unitless]
    safety_factor               Safety Factor in vehicle design                [Unitless]
    max_g_load                  Maximum g-forces load for certification        [UNitless]
    motor_efficiency:           Motor Efficiency                               [Unitless]
    
    Outputs:
    None
    
    Properties Used:
    N/A
    '''
    settings       = Data()

    settings.method_settings = Data()

    settings.method_settings.contingency_factor            = 1.1
    settings.method_settings.speed_of_sound                = 340.294
    settings.method_settings.max_tip_mach                  = 0.65
    settings.method_settings.disk_area_factor              = 1.15
    settings.method_settings.safety_factor                 = 1.5
    settings.method_settings.max_thrust_to_weight_ratio    = 1.1
    settings.method_settings.max_g_load                    = 3.8
    settings.method_settings.motor_efficiency              = 0.85*0.98

    breakdown      = empty(vehicle,settings)
    build_up_mass  = breakdown.total    
    diff           = vehicle.mass_properties.max_takeoff - build_up_mass
    iterations     = 0
    
    while(abs(diff)>1):
        vehicle.mass_properties.max_takeoff = vehicle.mass_properties.max_takeoff - diff
        
        # Note that 'diff' will be negative if buildup mass is larger than MTOW, so subtractive
        # iteration always moves MTOW toward buildup mass
        
        breakdown      = empty(vehicle,settings)
        build_up_mass  = breakdown.total    
        diff           = vehicle.mass_properties.max_takeoff - build_up_mass 
        iterations     += 1
        if print_iterations:
            print(round(diff,3))
        if iterations == 100:
            print('Weight convergence failed!')
            return False 
    print('Converged MTOW = ' + str(round(vehicle.mass_properties.max_takeoff)) + ' kg')
    
    return True 
