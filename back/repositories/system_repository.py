

from config.db import conectar_db

SYSTEM_NAME_MAP = {
    "price_display_system": "Price Display System",
    "corporate_lighting_system": "Corporate Lighting System",
    "canopy_lighting_system": "Canopy Lighting System",
    "perimeter_lighting_system": "Perimeter Lighting System",
    "office_and_general_services": "Office and General Services System",
    "submersible_pump_system": "Submersible Pump System",
    "fuel_dispenser_system": "Fuel Dispenser System",
    "air_conditioning_system - server_room": "Air Conditioning System - Server Room",
    "air_conditioning_system - office_area": "Air Conditioning System - Office Area",
    "customer_service_kiosk_system - refrigeration": "Customer Service Kiosk System - Refrigeration",
    "customer_service_kiosk_system - coffee_machine": "Customer Service Kiosk System - Coffee Machine",
}

def get_systems_map():
    
    connection = conectar_db()
    cursor = connection.cursor()

    cursor.execute("SELECT id, name FROM systems;")
    systems = cursor.fetchall()

    cursor.close()
    connection.close()

    db_name_to_id = {name: system_id for system_id, name in systems}

    systems_map = {}
    for internal_name, db_name in SYSTEM_NAME_MAP.items():
        system_id = db_name_to_id.get(db_name)
        if system_id:
            systems_map[internal_name] = system_id

    return systems_map






    