

import datetime
from domain_config.systems_config import SYSTEMS_CONFIG
from domain_config.working_schedules import WORKING_SCHEDULES


class ScheduleService:

    @staticmethod
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

    @staticmethod
    def get_schedule_for_system_name(system_name: str) -> str:
        if " - " not in system_name:
            components = SYSTEMS_CONFIG[system_name]["components"]
            comp_config = next(iter(components.values()))
            return comp_config["schedule"]

        parent, child = system_name.split(" - ", 1)
        return SYSTEMS_CONFIG[parent]["components"][child]["schedule"]

    @staticmethod
    def is_system_active(schedule_name: str, timestamp: datetime.datetime) -> bool:
        schedule = WORKING_SCHEDULES[schedule_name]
        return timestamp.weekday() in schedule["days"] and timestamp.hour in schedule["hours"]

    @staticmethod
    def is_system_name_active(system_name: str, timestamp: datetime.datetime) -> bool:
        schedule_name = ScheduleService.get_schedule_for_system_name(system_name)
        return ScheduleService.is_system_active(schedule_name, timestamp)