

from flask import Blueprint, jsonify
from services.simulation_service import (
    generate_daily_simulation,
    calculate_daily_totals
)

simulation_bp = Blueprint('simulation', __name__)

@simulation_bp.route ('/')
def index ():
    return "Energy monitoring system working correctly."

@simulation_bp.route('/daily')
def daily_simulation():
    daily_data = generate_daily_simulation()
    totals = calculate_daily_totals(daily_data)

    return jsonify({
        "hours_generated": 24,
        "records": daily_data,
        "totals": totals
    })
