

import datetime
from flask import Blueprint, jsonify
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

        if not system_id:
            continue

        hourly_records.append(
            (system_id, timestamp, consumption)
        )

    insert_hourly_consumption(hourly_records)

    daily_records = build_daily_consumption_records(hourly_records)

    return jsonify({
        "status": "ok",
        "simulation_date": simulation_date.isoformat(),
        "hours_generated": 24,
        "hourly_records_inserted": len(hourly_records),
        "daily_records_inserted": len(daily_records)
    }), 200
