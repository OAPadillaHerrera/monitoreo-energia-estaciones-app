

"""
References:

CREG Resolution 024 of 2005 (Colombia):
https://gestornormativo.creg.gov.co/Publicac.nsf/1c09d18d2d5ffb5b05256eee00709c02/7ef77a545ceb66680525785a007a6b88/$FILE/Creg024-2005.pdf

ANSI C84.1 Voltage Tolerance Standard (USA):
https://voltage-disturbance.com/voltage-quality/voltage-tolerance-standard-ansi-c84-1/
"""

import random

CORPORATE_LIGHTING_NOMINAL_POWER_KWH = 0.84
CORPORATE_LIGHTING_NOMINAL_VOLTAGE = 120
CORPORATE_LIGHTING_MIN_VOLTAGE = 114
CORPORATE_LIGHTING_MAX_VOLTAGE = 126


def get_hourly_corporate_lighting_consumption():

    voltage = random.uniform(

        CORPORATE_LIGHTING_MIN_VOLTAGE,
        CORPORATE_LIGHTING_MAX_VOLTAGE

    )

    real_consumption = (

        CORPORATE_LIGHTING_NOMINAL_POWER_KWH
        * voltage
        / CORPORATE_LIGHTING_NOMINAL_VOLTAGE
        
    )

    return real_consumption
