

"""
SystemCalculator Service

Calculates energy consumption for systems and their components,
considering:

- Nominal consumption per component
- Applied voltage (120V or 240V)
- Duration-based multipliers
- Time-slot based consumption factors

Supports both single-component and multi-component systems.
"""

import datetime
from typing import Dict, Union

from domain_config.systems_config import SYSTEMS_CONFIG
from electrical.consumption_slots import get_slot_factor

class SystemCalculator:


    @staticmethod
    def calculate(
        system_name: str,
        voltage_120v: float,
        voltage_240v: float,
        timestamp: datetime.datetime
    ) -> Union[float, Dict[str, float]]:

        if " - " in system_name:
            parent_name, component_name = system_name.split(" - ", 1)
            config = SYSTEMS_CONFIG[parent_name]["components"][component_name]

            return SystemCalculator._calculate_single(
                config,
                parent_name,
                component_name,
                voltage_120v,
                voltage_240v,
                timestamp,
            )

        components_config = SYSTEMS_CONFIG[system_name]["components"]

        if len(components_config) > 1:
            results: Dict[str, float] = {}

            for component_name, component_config in components_config.items():
                results[component_name] = SystemCalculator._calculate_single(
                    component_config,
                    system_name,
                    component_name,
                    voltage_120v,
                    voltage_240v,
                    timestamp,
                )

            return results

        component_name, component_config = next(iter(components_config.items()))

        return SystemCalculator._calculate_single(
            component_config,
            system_name,
            component_name,
            voltage_120v,
            voltage_240v,
            timestamp,
        )

    @staticmethod
    def _calculate_single(
        config: dict,
        parent_name: str,
        component_name: str,
        voltage_120v: float,
        voltage_240v: float,
        timestamp: datetime.datetime,
    ) -> float:

        nominal_power: float = config.get("nominal_consumption_kwh", 0.0)
        nominal_voltage: int = config["voltage"]
        applied_voltage: float = voltage_240v if nominal_voltage == 240 else voltage_120v

        if "duration_hours" in config:
            equivalent_daily_hours: float = config["duration_hours"] * 24
            daily_energy: float = nominal_power * equivalent_daily_hours

            slot_factor = get_slot_factor(parent_name, timestamp)

            if slot_factor is None:
                raise RuntimeError(
                    f"Missing consumption slot for {component_name} at {timestamp}"
                )

            return daily_energy * (applied_voltage / nominal_voltage) * slot_factor

        return nominal_power * (applied_voltage / nominal_voltage)