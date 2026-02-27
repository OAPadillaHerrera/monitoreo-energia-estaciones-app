

"""
Working Schedules Configuration

Defines the allowed working days and active hours for each schedule.
Used by ScheduleService to determine whether a system is active
at a given timestamp.
"""

from typing import Dict, List, TypedDict

class ScheduleConfig(TypedDict):
    days: List[int]   
    hours: List[int]  

WORKING_SCHEDULES: Dict[str, ScheduleConfig] = {
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
    },
}