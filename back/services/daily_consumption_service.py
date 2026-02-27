

"""
Daily Consumption Service

Aggregates hourly consumption records into daily totals per system 
and inserts them into the database.
"""

from collections import defaultdict
from datetime import datetime, date
from typing import List, Tuple

from repositories.daily_consumption_repository import insert_daily_consumption

def build_daily_consumption_records(
    hourly_records: List[Tuple[int, datetime, float]]
) -> List[Tuple[int, date, float]]:
    totals: defaultdict[Tuple[int, date], float] = defaultdict(float)

    for system_id, timestamp, consumption in hourly_records:
        key = (system_id, timestamp.date())
        totals[key] += consumption

    daily_records: List[Tuple[int, date, float]] = [
        (system_id, day, total) for (system_id, day), total in totals.items()
    ]
            
    insert_daily_consumption(daily_records)
    return daily_records
