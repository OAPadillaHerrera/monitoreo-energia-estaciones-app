

"""
References:

CREG Resolution 024 of 2005 (Colombia):
https://gestornormativo.creg.gov.co/Publicac.nsf/1c09d18d2d5ffb5b05256eee00709c02/7ef77a545ceb66680525785a007a6b88/$FILE/Creg024-2005.pdf

ANSI C84.1 Voltage Tolerance Standard (USA):
https://voltage-disturbance.com/voltage-quality/voltage-tolerance-standard-ansi-c84-1/
"""

from electrical.consumption_slots import get_slot_factor

FUEL_DISPENSER_SYSTEM_NOMINAL_POWER_KWH = 0.0275
FUEL_DISPENSER_SYSTEM_NOMINAL_VOLTAGE = 240
FUEL_DISPENSER_SYSTEM_EQUIVALENT_DAILY_HOURS = 2.05

def get_hourly_fuel_dispenser_system_consumption(voltage, timestamp):

    daily_energy = (
        FUEL_DISPENSER_SYSTEM_NOMINAL_POWER_KWH
        * FUEL_DISPENSER_SYSTEM_EQUIVALENT_DAILY_HOURS
    )
    
    slot_factor = get_slot_factor("fuel_dispenser_system", timestamp)

    if slot_factor is None:
        raise RuntimeError(
            f"Missing consumption slot for pumps at {timestamp}"
        )
    
    real_consumption = (

        daily_energy
        * (voltage / FUEL_DISPENSER_SYSTEM_NOMINAL_VOLTAGE)
        * slot_factor
        
    )

    return real_consumption