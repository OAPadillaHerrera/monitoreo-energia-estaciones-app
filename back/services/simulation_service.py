

import datetime
from systems.system_calculator import SystemCalculator
from schedules.schedule_service import ScheduleService


def _calculate_system_consumption(system_name, timestamp, voltage_120v, voltage_240v, zero_event):

    if not ScheduleService.is_system_name_active(system_name, timestamp):
        return 0.0

    if zero_event and zero_event.is_system_down(system_name, timestamp):
        return 0.0

    return SystemCalculator.calculate(system_name, voltage_120v, voltage_240v, timestamp)

def generate_hourly_consumption(timestamp, zero_event, voltage_120v, voltage_240v, system_names):

    return [
        (
            system_name,
            _calculate_system_consumption(
                system_name,
                timestamp,
                voltage_120v,
                voltage_240v,
                zero_event
            ),
            timestamp,
        )
        for system_name in system_names
    ]

def generate_daily_simulation(simulation_date, voltage_profile, zero_event, systems_map):

    voltage_profile.generate_daily_profile(simulation_date)
    zero_event.generate_monthly_event_if_needed(simulation_date, voltage_profile)

    base_time = datetime.datetime.combine(simulation_date, datetime.time.min)

    daily_data = []
    voltage_records = []
    event_records = []

    system_names = ScheduleService.get_all_system_names()

    for hour in range(24):
        timestamp = base_time.replace(hour=hour)

        voltage_120v = voltage_profile.get_voltage_120v(hour)
        voltage_240v = voltage_profile.get_voltage_240v(hour)
        quality_flag = voltage_profile.get_quality_flag(hour)

        voltage_records.append(
            (timestamp, voltage_120v, voltage_240v, quality_flag)
        )

        if zero_event.system_name and zero_event.start <= timestamp < zero_event.end:
            system_id = systems_map.get(zero_event.system_name)
            if system_id:
                event_records.append(
                    (timestamp, system_id, zero_event.EVENT_TYPE)
                )

        hourly_data = generate_hourly_consumption(
            timestamp,
            zero_event,
            voltage_120v,
            voltage_240v,
            system_names,
        )

        daily_data.extend(hourly_data)

    return daily_data, voltage_records, event_records

def generate_range_simulation(start_date, end_date, voltage_profile, zero_event, systems_map):

    all_hourly_data = []
    all_voltage_records = []
    all_event_records = []

    current_date = start_date

    while current_date <= end_date:

        daily_data, voltage_records, event_records = generate_daily_simulation(
            current_date,
            voltage_profile,
            zero_event,
            systems_map
        )

        all_hourly_data.extend(daily_data)
        all_voltage_records.extend(voltage_records)
        all_event_records.extend(event_records)

        current_date += datetime.timedelta(days=1)

    return {
        "hourly_data": all_hourly_data,
        "voltage_records": all_voltage_records,
        "event_records": all_event_records
    }

def calculate_daily_totals(daily_data):

    totals = {}

    for system_name, consumption, _ in daily_data:
        totals[system_name] = totals.get(system_name, 0.0) + consumption

    return totals
