

from domain_config.systems_config import SYSTEMS_CONFIG
from electrical.consumption_slots import get_slot_factor

class SystemCalculator:

    @staticmethod
    def calculate(system_name: str, voltage_120v: float, voltage_240v: float, timestamp):
        
        if " - " in system_name:
            parent, child = system_name.split(" - ", 1)
            config = SYSTEMS_CONFIG[parent]["components"][child]
            return SystemCalculator._calculate_single(config, parent, child, voltage_120v, voltage_240v, timestamp)

        config = SYSTEMS_CONFIG[system_name]["components"]

        if len(config) > 1:
            results = {}
            for sub_name, sub_config in config.items():
                results[sub_name] = SystemCalculator._calculate_single(sub_config, system_name, sub_name, voltage_120v, voltage_240v, timestamp)
            return results
        else:
            comp_name, comp_config = next(iter(config.items()))
            return SystemCalculator._calculate_single(comp_config, system_name, comp_name, voltage_120v, voltage_240v, timestamp)

    @staticmethod
    def _calculate_single(config, parent_name, comp_name, voltage_120v, voltage_240v, timestamp):
        nominal_power = config.get("nominal_consumption_kwh", 0.0)
        nominal_voltage = config["voltage"]
        voltage = voltage_240v if nominal_voltage == 240 else voltage_120v

        if "duration_hours" in config:
            equivalent_daily_hours = config["duration_hours"] * 24
            daily_energy = nominal_power * equivalent_daily_hours

            slot_system_name = parent_name
            slot_factor = get_slot_factor(slot_system_name, timestamp)
            if slot_factor is None:
                raise RuntimeError(f"Missing consumption slot for {comp_name} at {timestamp}")

            return daily_energy * (voltage / nominal_voltage) * slot_factor

        return nominal_power * (voltage / nominal_voltage)