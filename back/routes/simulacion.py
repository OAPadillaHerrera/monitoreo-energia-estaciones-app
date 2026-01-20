

from flask import Blueprint, jsonify
import datetime

simulacion_bp = Blueprint ('simulacion', __name__)

SYSTEMS_CONSUMPTION_PER_HOUR = {
    "Price Display System (LED Modules)": {
        "consumption": 2.04,
        "schedule": "24_7"
        },

    "Corporate Lighting System (LED Signage and Logo)": {
        "consumption": 0.84,
        "schedule": "24_7"
        },

    "Canopy Lighting System (27 Lamps)": {
        "consumption": 2.052,
        "schedule": "nighttime"
        },

    "Perimeter Lighting System (5 Luminaires)": {
        "consumption": 0.275,
        "schedule": "nighttime"
        },

    "Office and General Services System": {
        "consumption": 1.1,
        "schedule": "office_hours"
    },  

    "Submersible Pump System": {
        "consumption": 0.577,
        "schedule": "24_7",
        "duration_hours": 2.04
    },

    "Fuel Dispenser System (5 Units)": {
        "consumption": 0.0375,
        "schedule": "24_7",
        "duration_hours": 2.05
    },

    "Air Conditioning System": {
        "Server Room": {
            "consumption": 0.184,
            "schedule": "24_7"
        }        
    },

    "Customer Service Kiosk System": {
         "Refrigeration": {
            "consumption": 0.84,
            "schedule": "24_7"
        }     
    }
}   

WORKING_SCHEDULES = {
    "24_7": {
        "days": [0, 1, 2, 3, 4, 5, 6],
        "hours": range(0, 24),
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
        "hours": range(6, 7),
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

                duration = config.get("duration_hours", 1)
                real_consumption = config["consumption"] * duration

                data.append((system, real_consumption, timestamp))

        else:
            for sub_system, sub_config in config.items():
                if is_system_active(sub_config["schedule"], timestamp):

                    duration = sub_config.get("duration_hours", 1)
                    real_consumption = sub_config["consumption"] * duration

                    system_name = f"{system} - {sub_system}"

                    data.append(
                        (system_name, real_consumption, timestamp)
                    )
        
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

def generate_simulated_data():
    timestamp = datetime.datetime.now()
    data = generate_hourly_consumption(timestamp)

    print(f"Generated data: {data}")
    return data

@simulacion_bp.route ('/')
def index ():
    return "Energy monitoring system working correctly."


