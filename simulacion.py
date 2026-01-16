

from flask import Blueprint, jsonify
import datetime

simulacion_bp = Blueprint ('simulacion', __name__)

SYSTEMS_COMSUMPTION_PER_HOUR = {
    "Price Display System (LED Modules)": 2.04,
    "Corporate Lighting System (LED Signage and Logo)": 0.84,
    "Canopy Lighting System (27 Lamps)": 2.052,
    "Perimeter Lighting System (5 Luminaires)": 0.275,
    "Office and General Services System": 1.1,    
    "Submersible Pump System": 0.577,
    "Fuel Dispenser System (5 Units)": 0.0375,

    "Air Conditioning System": {
        "Server Room": 0.184, # 24/7
    },

    "Customer Service Kiosk System": {
        "Refrigeration": 0.84, # 24/7
    }
}   

def generate_hourly_consumption(timestamp):   
    data = []

    for system, consumption in SYSTEMS_COMSUMPTION_PER_HOUR.items():

        if isinstance(consumption, (int, float)):
            data.append((system, consumption, timestamp ))

        elif isinstance(consumption, dict):
            for sub_system, sub_consumption, in consumption.items():
                system_name = f"{system} - {sub_system}"
                data.append((system_name, sub_consumption, timestamp ))
        
    return data

def generate_simulated_data():
    timestamp = datetime.datetime.now()
    data = generate_hourly_consumption(timestamp)
    print(f"Generated data: {data}")
    return data

#...............................................#

@simulacion_bp.route ('/')
def index ():
    return "ENERGY MONITORING SYSTEM WORKING CORRECTLY ..."


