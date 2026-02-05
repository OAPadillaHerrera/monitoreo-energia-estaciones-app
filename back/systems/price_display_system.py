

"""
References:

CREG Resolution 024 of 2005 (Colombia):
https://gestornormativo.creg.gov.co/Publicac.nsf/1c09d18d2d5ffb5b05256eee00709c02/7ef77a545ceb66680525785a007a6b88/$FILE/Creg024-2005.pdf

ANSI C84.1 Voltage Tolerance Standard (USA):
https://voltage-disturbance.com/voltage-quality/voltage-tolerance-standard-ansi-c84-1/
"""


PRICE_DISPLAY_NOMINAL_POWER_KWH = 2.04
PRICE_DISPLAY_NOMINAL_VOLTAGE = 120

def get_hourly_price_display_consumption(voltage):

    real_consumption = (

        PRICE_DISPLAY_NOMINAL_POWER_KWH
        * voltage
        / PRICE_DISPLAY_NOMINAL_VOLTAGE

    )

    return real_consumption





