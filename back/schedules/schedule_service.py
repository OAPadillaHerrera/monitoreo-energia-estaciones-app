

"""
Schedule Service

Provides utilities to resolve system schedules and determine
whether a system (or component) is active at a given timestamp.

Integrates system configuration (SYSTEMS_CONFIG) with
working schedule definitions (WORKING_SCHEDULES).
"""

import datetime
from typing import List

from domain_config.systems_config import SYSTEMS_CONFIG
from domain_config.working_schedules import WORKING_SCHEDULES

class ScheduleService:

    @staticmethod
    def get_all_system_names() -> List[str]:
       
        names: List[str] = []

        for system_name, config in SYSTEMS_CONFIG.items():
            components = config["components"]

            if len(components) == 1:
                names.append(system_name)
            else:
                for component_name in components.keys():
                    names.append(f"{system_name} - {component_name}")

        return names

    @staticmethod
    def get_schedule_for_system_name(system_name: str) -> str:
       
        if " - " not in system_name:
            components = SYSTEMS_CONFIG[system_name]["components"]
            component_config = next(iter(components.values()))
            return component_config["schedule"]

        parent_name, component_name = system_name.split(" - ", 1)
        return SYSTEMS_CONFIG[parent_name]["components"][component_name]["schedule"]

    @staticmethod
    def is_system_active(
        schedule_name: str,
        timestamp: datetime.datetime
    ) -> bool:
     
        schedule = WORKING_SCHEDULES[schedule_name]

        return (
            timestamp.weekday() in schedule["days"]
            and timestamp.hour in schedule["hours"]
        )

    @staticmethod
    def is_system_name_active(
        system_name: str,
        timestamp: datetime.datetime
    ) -> bool:
       
        schedule_name = ScheduleService.get_schedule_for_system_name(system_name)
        return ScheduleService.is_system_active(schedule_name, timestamp)