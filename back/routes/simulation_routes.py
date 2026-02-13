

import datetime
from flask import Blueprint, jsonify, request
from services.simulation_service import generate_daily_simulation
from repositories.system_repository import get_systems_map

from repositories.consumption_repository import (
    insert_hourly_consumption,
    get_latest_consumption_date
)

from services.daily_consumption_service import build_daily_consumption_records
from electrical.voltage_profile import VoltageProfile
from electrical.zero_consumption_events import MonthlyZeroConsumptionEvent

simulation_bp = Blueprint('simulation', __name__)
voltage_profile = VoltageProfile()
zero_event = MonthlyZeroConsumptionEvent()

@simulation_bp.route('/')
def index():
    return "Energy monitoring system working correctly."

@simulation_bp.route('/daily', methods=['POST'])
def daily_simulation():

    today = datetime.date.today()
    latest_date = get_latest_consumption_date()

    if latest_date:
        simulation_date = latest_date + datetime.timedelta(days=1)
    else:
        simulation_date = today

    simulated_data = generate_daily_simulation(
        simulation_date=simulation_date,
        voltage_profile=voltage_profile,
        zero_event=zero_event
    )

    systems_map = get_systems_map()
    hourly_records = []

    for system_name, consumption, timestamp in simulated_data:
        system_id = systems_map.get(system_name)
        if system_id:
            hourly_records.append((system_id, timestamp, consumption))

    insert_hourly_consumption(hourly_records)
    daily_records = build_daily_consumption_records(hourly_records)

    return jsonify({
        "status": "ok",
        "simulation_date": simulation_date.isoformat(),
        "hours_generated": 24,
        "hourly_records_inserted": len(hourly_records),
        "daily_records_inserted": len(daily_records)
    }), 200


@simulation_bp.route('/range', methods=['POST'])
def range_simulation():

    payload = request.get_json() or {}
    start_date = datetime.date.fromisoformat(payload["start_date"])
    end_date = datetime.date.fromisoformat(payload["end_date"])

    latest_date = get_latest_consumption_date()

    if latest_date:
        first_missing_date = latest_date + datetime.timedelta(days=1)
    else:
        first_missing_date = start_date

    effective_start = max(start_date, first_missing_date)

    if effective_start > end_date:
        return jsonify({
            "status": "ok",
            "start_date": start_date.isoformat(),
            "end_date": end_date.isoformat(),
            "message": "No days to generate (range already exists in DB).",
            "hourly_records_inserted": 0,
            "daily_records_inserted": 0
        }), 200

    systems_map = get_systems_map()
    all_hourly_consumption = []

    zero_event = MonthlyZeroConsumptionEvent() 

    current_date = effective_start
    while current_date <= end_date:

        daily_data = generate_daily_simulation(
            simulation_date=current_date,
            voltage_profile=voltage_profile,
            zero_event=zero_event
        )

        for system_name, consumption, timestamp in daily_data:
            system_id = systems_map.get(system_name)
            if system_id:
                all_hourly_consumption.append((system_id, timestamp, consumption))

        current_date += datetime.timedelta(days=1)

    insert_hourly_consumption(all_hourly_consumption)
    all_daily_records = build_daily_consumption_records(all_hourly_consumption)

    return jsonify({
        "status": "ok",
        "start_date": start_date.isoformat(),
        "end_date": end_date.isoformat(),
        "effective_start_date": effective_start.isoformat(),
        "hourly_records_inserted": len(all_hourly_consumption),
        "daily_records_inserted": len(all_daily_records)
    }), 200




