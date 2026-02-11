

import datetime

SYSTEMS_CONSUMPTION_PER_HOUR = {

    "submersible_pump_system": {
        "consumption": 0.577,
        "duration_hours": 2.04
    },
    "fuel_dispenser_system": {
        "consumption": 0.0275,
        "duration_hours": 2.05
    },

}

AFFECTED_SYSTEMS = {

    "submersible_pump_system",
    "fuel_dispenser_system",

}

def get_daily_total_consumption(system_name: str) -> float:

    config = SYSTEMS_CONSUMPTION_PER_HOUR[system_name]

    base_consumption = config["consumption"]
    duration_hours = config.get("duration_hours", 1)

    return base_consumption * duration_hours

TIME_SLOTS = {

    "mon_fri": [
        {"name": "low",    "start": 0,  "end": 7,  "percentage": 0.18},
        {"name": "high",   "start": 7,  "end": 11, "percentage": 0.28},
        {"name": "medium", "start": 11, "end": 17, "percentage": 0.20},
        {"name": "high",   "start": 17, "end": 20, "percentage": 0.28},
        {"name": "low",    "start": 20, "end": 24, "percentage": 0.06},
    ],

    "saturday": [
        {"name": "low",    "start": 0,  "end": 7,  "percentage": 0.25},
        {"name": "high",   "start": 7,  "end": 11, "percentage": 0.35},
        {"name": "medium", "start": 11, "end": 13, "percentage": 0.20},
        {"name": "low",    "start": 13, "end": 24, "percentage": 0.20},
    ],

    "sunday": [
        {"name": "low",    "start": 0,  "end": 24, "percentage": 1.00},
    ],

}

def get_day_type(timestamp: datetime.datetime) -> str:
    
    weekday = timestamp.weekday()  

    if weekday < 5:
        return "mon_fri"
    elif weekday == 5:
        return "saturday"
    else:
        return "sunday"

def get_slot_factor(system_name: str, timestamp: datetime.datetime):

    if system_name not in AFFECTED_SYSTEMS:
        return None

    day_type = get_day_type(timestamp)
    slots = TIME_SLOTS[day_type]

    current_hour = timestamp.hour

    for slot in slots:

        if slot["start"] <= current_hour < slot["end"]:
            
            hours_in_slot = slot["end"] - slot["start"]

            slot_factor = slot["percentage"] / hours_in_slot

            return slot_factor

    return None




