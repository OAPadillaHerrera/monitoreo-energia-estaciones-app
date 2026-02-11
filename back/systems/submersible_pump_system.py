

"""
References:

CREG Resolution 024 of 2005 (Colombia):
https://gestornormativo.creg.gov.co/Publicac.nsf/1c09d18d2d5ffb5b05256eee00709c02/7ef77a545ceb66680525785a007a6b88/$FILE/Creg024-2005.pdf

ANSI C84.1 Voltage Tolerance Standard (USA):
https://voltage-disturbance.com/voltage-quality/voltage-tolerance-standard-ansi-c84-1/
"""

from electrical.consumption_slots import get_slot_factor

SUBMERSIBLE_PUMP_SYSTEM_NOMINAL_POWER_KWH = 0.577
SUBMERSIBLE_PUMP_SYSTEM_NOMINAL_VOLTAGE = 240
SUBMERSIBLE_PUMP_SYSTEM_EQUIVALENT_DAILY_HOURS = 2.04

def get_hourly_submersible_pump_system_consumption(voltage, timestamp):

    daily_energy = (
        SUBMERSIBLE_PUMP_SYSTEM_NOMINAL_POWER_KWH
        * SUBMERSIBLE_PUMP_SYSTEM_EQUIVALENT_DAILY_HOURS
    )

    slot_factor = get_slot_factor("submersible_pump_system", timestamp)

    if slot_factor is None:

        raise RuntimeError(
            f"Missing consumption slot for pumps at {timestamp}"
        )

    real_consumption = (

        daily_energy
        * (voltage / SUBMERSIBLE_PUMP_SYSTEM_NOMINAL_VOLTAGE)
        * slot_factor        
    )

    return real_consumption