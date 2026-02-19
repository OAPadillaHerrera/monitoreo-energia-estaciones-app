

import datetime
from systems.system_calculator import SystemCalculator
from repositories.voltage_repository import insert_hourly_voltage
from repositories.system_repository import get_systems_map
from repositories.system_events_repository import insert_system_events
from electrical.zero_consumption_events import MonthlyZeroConsumptionEvent
from domain_config.systems_config import SYSTEMS_CONFIG
from domain_config.working_schedules import WORKING_SCHEDULES


def is_system_active(schedule_name: str, timestamp: datetime.datetime) -> bool:
    schedule = WORKING_SCHEDULES[schedule_name]
    return (
        timestamp.weekday() in schedule["days"]
        and timestamp.hour in schedule["hours"]
    )

def get_schedule_for_system_name(system_name: str) -> str:
    if " - " not in system_name:
        components = SYSTEMS_CONFIG[system_name]["components"]
        comp_config = next(iter(components.values()))
        return comp_config["schedule"]

    parent, child = system_name.split(" - ", 1)
    return SYSTEMS_CONFIG[parent]["components"][child]["schedule"]

def is_system_name_active(system_name: str, timestamp: datetime.datetime) -> bool:
    schedule_name = get_schedule_for_system_name(system_name)
    return is_system_active(schedule_name, timestamp)

def get_all_system_names():
    names = []

    for system, config in SYSTEMS_CONFIG.items():
        components = config["components"]

        if len(components) == 1:
            names.append(system)

        else:
            for sub_system in components.keys():
                names.append(f"{system} - {sub_system}")

    return names

def generate_hourly_consumption(
    timestamp: datetime.datetime,
    voltage_profile,
    zero_event: MonthlyZeroConsumptionEvent,
):
    data = []

    hour = timestamp.hour
    voltage_120v = voltage_profile.get_voltage_120v(hour)
    voltage_240v = voltage_profile.get_voltage_240v(hour)

    for system_name in get_all_system_names():

        if not is_system_name_active(system_name, timestamp):
            real_consumption = 0.0

        elif zero_event and zero_event.is_system_down(system_name, timestamp):
            real_consumption = 0.0

        else:
            real_consumption = SystemCalculator.calculate(
                system_name,
                voltage_120v,
                voltage_240v,
                timestamp,
            )

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
        systems_consumption_per_hour=SYSTEMS_CONFIG,
        working_schedules=WORKING_SCHEDULES,
        voltage_profile=voltage_profile,
    )

    base_time = datetime.datetime.combine(
        simulation_date,
        datetime.time.min,
    )

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
            quality_flag=quality_flag,
        )

        if zero_event.system_name:
            if zero_event.start <= timestamp < zero_event.end:

                systems_map = get_systems_map()
                system_id = systems_map.get(zero_event.system_name)

                if system_id:
                    insert_system_events(
                        [(timestamp, system_id, "monthly_zero_consumption")]
                    )

        hourly_data = generate_hourly_consumption(
            timestamp,
            voltage_profile,
            zero_event,
        )

        daily_data.extend(hourly_data)

    return daily_data

def generate_range_simulation(
    start_date,
    end_date,
    voltage_profile,
    zero_event: MonthlyZeroConsumptionEvent,
):
    all_hourly_data = []
    current_date = start_date

    while current_date <= end_date:
        daily_data = generate_daily_simulation(
            current_date,
            voltage_profile,
            zero_event,
        )

        all_hourly_data.extend(daily_data)
        current_date += datetime.timedelta(days=1)

    return all_hourly_data

def calculate_daily_totals(daily_data):
    totals = {}

    for system, consumption, _ in daily_data:
        if system not in totals:
            totals[system] = 0.0

        totals[system] += consumption

    return totals





