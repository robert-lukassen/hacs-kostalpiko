"""Constants for the Kostal Piko integration."""
from datetime import timedelta

from homeassistant.const import (
    UnitOfPower,
    UnitOfEnergy,
    UnitOfElectricPotential,
    UnitOfElectricCurrent,
)

DOMAIN = "kostalpiko"

DEFAULT_NAME = "Kostal Piko"

MIN_TIME_BETWEEN_UPDATES = timedelta(seconds=10)

SENSOR_TYPES = {
    "current_power": ["Current power", UnitOfPower.WATT, "mdi:solar-power", "measurement", "power"],
    "total_energy": ["Total energy", UnitOfEnergy.KILO_WATT_HOUR, "mdi:solar-power", "total_increasing", "energy"],
    "daily_energy": ["Daily energy", UnitOfEnergy.KILO_WATT_HOUR, "mdi:solar-power", "total_increasing", "energy"],
    "dc_1_voltage": ["String 1 DC voltage",  UnitOfElectricPotential.VOLT, "mdi:current-ac", "measurement", "voltage"],
    "dc_1_current": ["String 1 DC current", UnitOfElectricCurrent.AMPERE, "mdi:flash", "measurement", "current"],
    "dc_1_power": ["String 1 DC power", UnitOfElectricCurrent.WATT, "mdi:solar-power", "measurement", "power"],
    "dc_2_voltage": ["String 1 DC voltage",  UnitOfElectricPotential.VOLT, "mdi:current-ac", "measurement", "voltage"],
    "dc_2_current": ["String 1 DC current", UnitOfElectricCurrent.AMPERE, "mdi:flash", "measurement", "current"],
    "dc_2_power": ["String 1 DC power", UnitOfElectricCurrent.WATT, "mdi:solar-power", "measurement", "power"],
    "dc_3_voltage": ["String 1 DC voltage",  UnitOfElectricPotential.VOLT, "mdi:current-ac", "measurement", "voltage"],
    "dc_3_current": ["String 1 DC current", UnitOfElectricCurrent.AMPERE, "mdi:flash", "measurement", "current"],
    "dc_3_power": ["String 1 DC power", UnitOfElectricCurrent.WATT, "mdi:solar-power", "measurement", "power"],
    "ac_1_voltage": ["Phase 1 AC voltage",  UnitOfElectricPotential.VOLT, "mdi:current-ac", "measurement", "voltage"],
    "ac_1_current": ["Phase 1 AC current", UnitOfElectricCurrent.AMPERE, "mdi:flash", "measurement", "current"],
    "ac_1_power": ["Phase 1 AC power", UnitOfElectricCurrent.WATT, "mdi:solar-power", "measurement", "power"],
    "ac_2_voltage": ["Phase 2 AC voltage",  UnitOfElectricPotential.VOLT, "mdi:current-ac", "measurement", "voltage"],
    "ac_2_current": ["Phase 2 AC current", UnitOfElectricCurrent.AMPERE, "mdi:flash", "measurement", "current"],
    "ac_2_power": ["Phase 2 AC power", UnitOfElectricCurrent.WATT, "mdi:solar-power", "measurement", "power"],
    "ac_3_voltage": ["Phase 3 AC voltage",  UnitOfElectricPotential.VOLT, "mdi:current-ac", "measurement", "voltage"],
    "ac_3_current": ["Phase 3 AC current", UnitOfElectricCurrent.AMPERE, "mdi:flash", "measurement", "current"],
    "ac_3_power": ["Phase 3 AC power", UnitOfElectricCurrent.WATT, "mdi:solar-power", "measurement", "power"],
    "status": ["Status", None, "mdi:solar-power", None, None],
}
