

from domain_config.systems_config import SYSTEMS_CONFIG
from domain_config.working_schedules import WORKING_SCHEDULES


class ScheduleService:

    @staticmethod
    def is_system_active(system_name: str, timestamp) -> bool:
      
        schedule_name = ScheduleService._get_schedule_for_system(system_name)
        schedule = WORKING_SCHEDULES.get(schedule_name)

        if not schedule:
            raise ValueError(f"Schedule '{schedule_name}' not found.")

        return (
            timestamp.weekday() in schedule["days"]
            and timestamp.hour in schedule["hours"]
        )

    @staticmethod
    def _get_schedule_for_system(system_name: str) -> str:

        if " - " in system_name:
            parent, component = system_name.split(" - ", 1)
            return SYSTEMS_CONFIG[parent]["components"][component]["schedule"]

        components = SYSTEMS_CONFIG[system_name]["components"]
        component_config = next(iter(components.values()))
        return component_config["schedule"]