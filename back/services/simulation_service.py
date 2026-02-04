

import datetime

from systems.coffee_machine import get_daily_coffee_machine_consumption
from systems.price_display_system import get_hourly_price_display_consumption
from systems.corporate_lighting_system import get_hourly_corporate_lighting_consumption
from systems.canopy_lighting_system import get_hourly_canopy_lighting_consumption
from systems.perimeter_lighting_system import get_hourly_perimeter_lighting_consumption
from systems.office_and_general_services import get_hourly_office_and_general_services_consumption
from systems.air_conditioning_system import get_hourly_air_conditioning_consumption


SYSTEMS_CONSUMPTION_PER_HOUR = {
    "price_display_system": {
        "description":"LED price display modules",
        "consumption": 2.04,
        "schedule": "24_7"
        },

    "corporate_lighting_system": {
        "description":"LED signage and corporate logo",
        "consumption": 0.84,
        "schedule": "nighttime"
        },

    "canopy_lighting_system": {
        "description":"27 canopy lamps",
        "units":27,        
        "consumption": 2.052,
        "schedule": "nighttime"
        },

    "perimeter_lighting_system": {
        "description": "5 perimeter luminaires",
        "units": 5,
        "consumption": 0.275,
        "schedule": "nighttime"
        },

    "office_and_general_services": {
        "consumption": 1.1,
        "schedule": "office_hours",
    },  

    "submersible_pump_system": {
        "description": "3 submersible pumps",
        "units": 3,
        "consumption": 0.577,
        "schedule": "24_7",
        "duration_hours": 2.04 / 24
    },

    "fuel_dispenser_system": {
        "description": "5 fuel dispensers",
        "units": 5,
        "consumption": 0.0275,
        "schedule": "24_7",
        "duration_hours": 2.05 / 24
    },

    "air_conditioning_system": {
        "server_room": {
            "consumption": 0.09183,
            "schedule": "24_7"
        },      
        "office_area": {
            "consumption": 0.09183,
            "schedule": "office_hours"
        }        
    },

    "customer_service_kiosk_system": {
         "refrigeration": {
            "description": "3 beverage coolers",
            "units": 3,
            "consumption": 0.125,
            "schedule": "24_7"
        },        
         "coffee_machine": {
            "schedule": "coffee_machine",
        },  
    }
}   

WORKING_SCHEDULES = {
    "24_7": {
        "days": [0, 1, 2, 3, 4, 5, 6],
        "hours": list(range(0, 24)),
    },

    "office_hours": {
        "days": [0, 1, 2, 3, 4],
        "hours": list(range(8, 12)) + list(range(13, 17)),
    },

    "nighttime": {
        "days": [0, 1, 2, 3, 4, 5, 6],
        "hours": list(range(18, 24)) + list(range(0, 6)),
    },

    "coffee_machine": {
        "days": [0, 1, 2, 3, 4, 5, 6],
        "hours": list(range(6, 7)),
    }
}

def is_system_active(schedule_name, timestamp):
    schedule = WORKING_SCHEDULES[schedule_name]
    return (
        timestamp.weekday() in schedule["days"]
        and timestamp.hour in schedule["hours"]
    )

def generate_hourly_consumption(timestamp):   

    data = []

    for system, config in SYSTEMS_CONSUMPTION_PER_HOUR.items():

        if "consumption" in config:

            if is_system_active(config["schedule"], timestamp):

                if system == "price_display_system":

                    real_consumption = get_hourly_price_display_consumption()

                elif system == "corporate_lighting_system":

                    real_consumption = get_hourly_corporate_lighting_consumption()

                elif system == "canopy_lighting_system":

                    real_consumption = get_hourly_canopy_lighting_consumption()

                elif system == "perimeter_lighting_system":

                    real_consumption = get_hourly_perimeter_lighting_consumption()

                elif system == "office_and_general_services":

                    real_consumption = get_hourly_office_and_general_services_consumption()

                else:

                    duration = config.get("duration_hours", 1)
                    real_consumption = config["consumption"] * duration

                data.append((system, real_consumption, timestamp))

        else:

            for sub_system, sub_config in config.items():

                if is_system_active(sub_config["schedule"], timestamp):

                    if sub_system == "coffee_machine":
                        
                        real_consumption = get_daily_coffee_machine_consumption()

                    elif sub_system == "server_room":

                        real_consumption = get_hourly_air_conditioning_consumption()

                    elif sub_system == "office_area":    
                        
                        real_consumption = get_hourly_air_conditioning_consumption()
                        
                    else:

                        duration = sub_config.get("duration_hours", 1)
                        real_consumption = sub_config["consumption"] * duration

                    system_name = f"{system} - {sub_system}"
                    data.append((system_name, real_consumption, timestamp))                    
        
    return data

def generate_daily_simulation():
    base_time = datetime.datetime.now().replace(minute=0, second=0)

    daily_data = []

    for hour in range(24):
        timestamp = base_time.replace(hour=hour)
        hourly_data = generate_hourly_consumption(timestamp)
        daily_data.extend(hourly_data)

    return daily_data

def calculate_daily_totals (daily_data):
    totals = {}

    for system, consumption, _ in daily_data:
        if system not in totals:
            totals[system] = 0

        totals[system] += consumption

    return totals    


