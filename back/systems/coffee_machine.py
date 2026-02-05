

"""
Reference coffee machine (technical guide):
https://www.hogaruniversal.com/cafetera-institucional-40tz/p
"""

import random


COFFEE_MACHINE_NOMINAL_POWER_KWH = 0.5
COFFEE_MACHINE_NOMINAL_VOLTAGE = 120  
COFFEE_MACHINE_MIN_VOLTAGE = 114
COFFEE_MACHINE_MAX_VOLTAGE = 126

def get_hourly_coffee_machine_consumption():

    voltage = random.uniform(

        COFFEE_MACHINE_MIN_VOLTAGE,
        COFFEE_MACHINE_MAX_VOLTAGE

    )

    real_consumption_per_voltage_variation = (

        COFFEE_MACHINE_NOMINAL_POWER_KWH
        * voltage
        / COFFEE_MACHINE_NOMINAL_VOLTAGE
        
    )

    return real_consumption_per_voltage_variation