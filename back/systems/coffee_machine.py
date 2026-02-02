

#Reference coffee machine (technical guide):
#https://www.hogaruniversal.com/cafetera-institucional-40tz/p

import random

COFFEE_MACHINE_BASE_CONSUMPTION_KWH = 0.5
COFFEE_MACHINE_NOMINAL_TIME_MIN = 30  
COFFEE_MACHINE_MIN_TIME_MIN = 25
COFFEE_MACHINE_MAX_TIME_MIN = 35

def get_daily_coffee_machine_consumption():

    minutes = random.uniform(
        COFFEE_MACHINE_MIN_TIME_MIN,
        COFFEE_MACHINE_MAX_TIME_MIN
    )

    consumption_per_minute = (
        COFFEE_MACHINE_BASE_CONSUMPTION_KWH
        / COFFEE_MACHINE_NOMINAL_TIME_MIN
    )

    return consumption_per_minute * minutes