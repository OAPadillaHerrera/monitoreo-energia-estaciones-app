

import datetime
from systems.coffee_machine import get_hourly_coffee_machine_consumption
from systems.price_display_system import get_hourly_price_display_consumption
from systems.corporate_lighting_system import get_hourly_corporate_lighting_consumption
from systems.canopy_lighting_system import get_hourly_canopy_lighting_consumption
from systems.perimeter_lighting_system import get_hourly_perimeter_lighting_consumption
from systems.office_and_general_services import get_hourly_office_and_general_services_consumption
from systems.air_conditioning_system import get_hourly_air_conditioning_consumption
from systems.refrigeration import get_hourly_refrigeration_consumption
from systems.submersible_pump_system import get_hourly_submersible_pump_system_consumption
from systems.fuel_dispenser_system import get_hourly_fuel_dispenser_system_consumption
from repositories.voltage_repository import insert_hourly_voltage
from repositories.system_repository import get_systems_map
from repositories.system_events_repository import insert_system_events
from electrical.zero_consumption_events import MonthlyZeroConsumptionEvent

SYSTEMS_CONSUMPTION_PER_HOUR = {
    "price_display_system": {
        "description": "LED price display modules",
        "consumption": 2.04,
        "schedule": "24_7"
    },
    "corporate_lighting_system": {
        "description": "LED signage and corporate logo",
        "consumption": 0.84,
        "schedule": "nighttime"
    },
    "canopy_lighting_system": {
        "description": "27 canopy lamps",
        "units": 27,
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
    return timestamp.weekday() in schedule["days"] and timestamp.hour in schedule["hours"]

def get_schedule_for_system_name(system_name: str) -> str:
    if " - " not in system_name:
        return SYSTEMS_CONSUMPTION_PER_HOUR[system_name]["schedule"]
    parent, child = system_name.split(" - ", 1)
    return SYSTEMS_CONSUMPTION_PER_HOUR[parent][child]["schedule"]

def is_system_name_active(system_name: str, timestamp) -> bool:
    schedule_name = get_schedule_for_system_name(system_name)
    return is_system_active(schedule_name, timestamp)

def get_all_system_names():
    names = []
    for system, config in SYSTEMS_CONSUMPTION_PER_HOUR.items():
        if "consumption" in config:
            names.append(system)
        else:
            for sub_system in config.keys():
                names.append(f"{system} - {sub_system}")
    return names

def generate_hourly_consumption(timestamp, voltage_profile, zero_event: MonthlyZeroConsumptionEvent):
    data = []
    hour = timestamp.hour
    voltage_120v = voltage_profile.get_voltage_120v(hour)
    voltage_240v = voltage_profile.get_voltage_240v(hour)

    for system, config in SYSTEMS_CONSUMPTION_PER_HOUR.items():
        if "consumption" in config: 
            system_name = system
            is_active = is_system_active(config["schedule"], timestamp)
            if not is_active:
                real_consumption = 0.0
            else:
                if zero_event and zero_event.is_system_down(system_name, timestamp):
                    real_consumption = 0.0
                else:
                    if system == "price_display_system":
                        real_consumption = get_hourly_price_display_consumption(voltage_120v)
                    elif system == "corporate_lighting_system":
                        real_consumption = get_hourly_corporate_lighting_consumption(voltage_120v)
                    elif system == "canopy_lighting_system":
                        real_consumption = get_hourly_canopy_lighting_consumption(voltage_120v)
                    elif system == "perimeter_lighting_system":
                        real_consumption = get_hourly_perimeter_lighting_consumption(voltage_120v)
                    elif system == "office_and_general_services":
                        real_consumption = get_hourly_office_and_general_services_consumption(voltage_120v)
                    elif system == "submersible_pump_system":
                        real_consumption = get_hourly_submersible_pump_system_consumption(voltage_240v, timestamp)
                    elif system == "fuel_dispenser_system":
                        real_consumption = get_hourly_fuel_dispenser_system_consumption(voltage_240v, timestamp)
                    else:
                        duration = config.get("duration_hours", 1)
                        real_consumption = config["consumption"] * duration
            data.append((system_name, real_consumption, timestamp))
        else:  
            for sub_system, sub_config in config.items():
                system_name = f"{system} - {sub_system}"
                is_active = is_system_active(sub_config["schedule"], timestamp)
                if not is_active:
                    real_consumption = 0.0
                else:
                    if zero_event and zero_event.is_system_down(system_name, timestamp):
                        real_consumption = 0.0
                    else:
                        if sub_system == "coffee_machine":
                            real_consumption = get_hourly_coffee_machine_consumption(voltage_120v)
                        elif sub_system == "server_room":
                            real_consumption = get_hourly_air_conditioning_consumption(voltage_120v)
                        elif sub_system == "office_area":
                            real_consumption = get_hourly_air_conditioning_consumption(voltage_120v)
                        elif sub_system == "refrigeration":
                            real_consumption = get_hourly_refrigeration_consumption(voltage_120v)
                        else:
                            duration = sub_config.get("duration_hours", 1)
                            real_consumption = sub_config["consumption"] * duration
                data.append((system_name, real_consumption, timestamp))
    return data

def generate_daily_simulation(
    simulation_date,
    voltage_profile,
    zero_event: MonthlyZeroConsumptionEvent,
):

    voltage_profile.generate_daily_profile(simulation_date)

    zero_event.generate_monthly_event_if_needed(
        simulation_date=simulation_date,
        systems_consumption_per_hour=SYSTEMS_CONSUMPTION_PER_HOUR,
        working_schedules=WORKING_SCHEDULES,
        voltage_profile=voltage_profile,
    )

    base_time = datetime.datetime.combine(simulation_date, datetime.time.min)
    daily_data = []

    for hour in range(24):
        timestamp = base_time.replace(hour=hour)

        voltage_120v = voltage_profile.get_voltage_120v(hour)
        voltage_240v = voltage_profile.get_voltage_240v(hour)
        quality_flag = voltage_profile.get_quality_flag(hour)

        insert_hourly_voltage(
            timestamp=timestamp,
            voltage_120v=voltage_120v,
            voltage_240v=voltage_240v,
            quality_flag=quality_flag
        )

        if zero_event.system_name and zero_event.start <= timestamp < zero_event.end:
            systems_map = get_systems_map()
            system_id = systems_map.get(zero_event.system_name)
            if system_id:
                insert_system_events([(timestamp, system_id, "monthly_zero_consumption")])

        hourly_data = generate_hourly_consumption(timestamp, voltage_profile, zero_event)
        daily_data.extend(hourly_data)

    return daily_data

def calculate_daily_totals(daily_data):
    totals = {}
    for system, consumption, _ in daily_data:
        if system not in totals:
            totals[system] = 0.0
        totals[system] += consumption
    return totals






