

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
        "schedule": "nightime"
        },

    "Perimeter Lighting System (5 Luminaires)": {
        "consumption": 0.275,
        "schedule": "nightime"
        },

    "Office and General Services System": {
        "consumption": 1.1,
        "schedule": "office_hours"
    },  

    "Submersible Pump System": {
        "consumption": 0.577,
        "schedule": "24_7"
    },

    "Fuel Dispenser System (5 Units)": {
        "consumption": 0.0375,
        "schedule": "24_7"
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
                data.append((system, config["consumption"], timestamp))

        else:
            for sub_system, sub_config in config.items():
                if is_system_active(sub_config["schedule"], timestamp):
                    system_name = f"{system} - {sub_system}"
                    data.append(
                        (system_name, sub_config["consumption"], timestamp)
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

def generate_simulated_data():
    timestamp = datetime.datetime.now()
    data = generate_hourly_consumption(timestamp)

    print(f"Generated data: {data}")
    return data

@simulacion_bp.route ('/')
def index ():
    return "ENERGY MONITORING SYSTEM WORKING CORRECTLY ..."


