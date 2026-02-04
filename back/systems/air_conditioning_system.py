

"""
References:

CREG Resolution 024 of 2005 (Colombia):
https://gestornormativo.creg.gov.co/Publicac.nsf/1c09d18d2d5ffb5b05256eee00709c02/7ef77a545ceb66680525785a007a6b88/$FILE/Creg024-2005.pdf

ANSI C84.1 Voltage Tolerance Standard (USA):
https://voltage-disturbance.com/voltage-quality/voltage-tolerance-standard-ansi-c84-1/
"""

import random

AIR_CONDITIONING_NOMINAL_POWER_KWH = 0.09183
AIR_CONDITIONING_NOMINAL_VOLTAGE = 120
AIR_CONDITIONING_MIN_VOLTAGE = 114
AIR_CONDITIONING_MAX_VOLTAGE = 126


def get_hourly_air_conditioning_consumption():

    voltage = random.uniform(

        AIR_CONDITIONING_MIN_VOLTAGE,
        AIR_CONDITIONING_MAX_VOLTAGE

    )

    real_consumption = (

        AIR_CONDITIONING_NOMINAL_POWER_KWH
        * voltage
        / AIR_CONDITIONING_NOMINAL_VOLTAGE
        
    )

    return real_consumption