

from collections import defaultdict
from repositories.daily_consumption_repository import insert_daily_consumption

def build_daily_consumption_records(hourly_records):

    totals = defaultdict (float)

    for system_id, timestamp, consumption in hourly_records:
        key = (system_id, timestamp.date())
        totals[key] += consumption

    daily_records = []

    for (system_id, day), total in totals.items():
        daily_records.append((system_id, day, total))
            
    insert_daily_consumption(daily_records)
    return daily_records

