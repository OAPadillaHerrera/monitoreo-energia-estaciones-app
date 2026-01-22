

import datetime
from flask import Blueprint, jsonify

from services.simulation_service import generate_daily_simulation
from repositories.system_repository import get_systems_map
from repositories.consumption_repository import (
    insert_hourly_consumption,
    exists_hourly_consumption_for_date
)
from services.daily_consumption_service import build_daily_consumption_records

simulation_bp = Blueprint('simulation', __name__)

@simulation_bp.route('/')
def index():
    return "Energy monitoring system working correctly."

@simulation_bp.route('/daily', methods=['POST'])
def daily_simulation():

    today = datetime.date.today()

    if exists_hourly_consumption_for_date(today):
        return jsonify({
            "status": "skipped",
            "message": "Daily simulation already exists for today."
        }),200

    simulated_data = generate_daily_simulation()
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
    
    daily_records = build_daily_consumption_records

    return jsonify({
        "status": "ok",
        "hours_generated": 24,
        "hourly_records_inserted": len(hourly_records),
        "daily_records_inserted": len(daily_records)
    }), 200
