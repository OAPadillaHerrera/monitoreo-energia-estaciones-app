

"""
Reference coffee machine (technical guide):
https://www.hogaruniversal.com/cafetera-institucional-40tz/p
"""


COFFEE_MACHINE_NOMINAL_POWER_KWH = 0.5
COFFEE_MACHINE_NOMINAL_VOLTAGE = 120  

def get_hourly_coffee_machine_consumption(voltage):

    real_consumption_per_voltage_variation = (

        COFFEE_MACHINE_NOMINAL_POWER_KWH
        * voltage
        / COFFEE_MACHINE_NOMINAL_VOLTAGE
        
    )

    return real_consumption_per_voltage_variation