"""The Kostal piko integration."""


import logging

from homeassistant.const import (
    CONF_USERNAME,
    CONF_PASSWORD,
    CONF_HOST,
    CONF_MONITORED_CONDITIONS,
)

from homeassistant.helpers.entity import Entity
from homeassistant.util import Throttle


from .const import SENSOR_TYPES, MIN_TIME_BETWEEN_UPDATES, DOMAIN

from kostalpiko import KostalPiko, KostalPikoReport

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, entry, async_add_entities):
     """Add an Kostal piko entry."""
     # Add the needed sensors to hass
     hasspiko = HassPiko(entry.data[CONF_HOST], hass)
     await hasspiko.async_update()
     entities = []
     for sensor in entry.data[CONF_MONITORED_CONDITIONS]:
         entities.append(PikoEntity(hasspiko, sensor, entry.title))
     async_add_entities(entities)

class PikoEntity(Entity):
    """Representation of a Piko inverter measurement."""

    def __init__(self, hasspiko, sensor_type, name):
        """Initialize the sensor."""
        self.serial_number = None
        self.model = None
        self._sensor = SENSOR_TYPES[sensor_type][0]
        self._name = name
        self.type = sensor_type
        self.hasspiko = hasspiko
        self._state = None
        self._unit_of_measurement = SENSOR_TYPES[self.type][1]
        self._icon = SENSOR_TYPES[self.type][2]
        # self._device_class = SENSOR_TYPES[self.type][4]
        if self._unit_of_measurement is not None:
            self._state_class = {"state_class": SENSOR_TYPES[self.type][3],"device_class":SENSOR_TYPES[self.type][4]}
        #self.update()

    @property
    def name(self):
        """Return the name of the sensor."""
        return "{} {}".format(self._name, self._sensor)

    @property
    def state(self):
        """Return the state of the device."""
        return self._state

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement this sensor expresses itself in."""
        return self._unit_of_measurement

    @property
    def icon(self):
        """Return icon."""
        return self._icon

    @property
    def unique_id(self):
        """Return unique id based on device serial and variable."""
        return "{} {}".format(self.serial_number, self._sensor)

    @property
    def device_info(self):
        """Return information about the device."""
        return {
            "identifiers": {(DOMAIN, self.serial_number)},
            "name": self._name,
            "manufacturer": "Kostal",
            "model": self.model,
        }

    @property
    def state_attributes(self):
        """Return device specific state attributes."""
        if self._unit_of_measurement is not None:
            return self._state_class

    async def async_update(self):
        """Update data."""
        await self.hasspiko.async_update()
        report = self.hasspiko.report
        info = self.hasspiko.info
        if info is not None:
            self.serial_number = info.serial_no
            self.model = info.typ
        if report is not None:
            if self.type == "current_power":
                self._state = report.ac_power[0] + report.ac_power[1] + report.ac_power[2]
            elif self.type == "total_energy":
                self._state = report.total_yield
            elif self.type == "daily_energy":
                self._state = report.daily_yield
            elif self.type == "dc_1_voltage":
                self._state = report.dc_voltage[0]
            elif self.type == "dc_2_voltage":
                self._state = report.dc_voltage[1]
            elif self.type == "dc_3_voltage":
                self._state = report.dc_voltage[2]
            elif self.type == "dc_1_current":
                self._state = report.dc_current[0]
            elif self.type == "dc_2_current":
                self._state = report.dc_current[1]
            elif self.type == "dc_3_current":
                self._state = report.dc_current[2]
            elif self.type == "dc_1_power":
                self._state = report.dc_power[0]
            elif self.type == "dc_2_power":
                self._state = report.dc_power[1]
            elif self.type == "dc_3_power":
                self._state = report.dc_power[2]
            elif self.type == "ac_1_voltage":
                self._state = report.ac_voltage[0]
            elif self.type == "ac_2_voltage":
                self._state = report.ac_voltage[1]
            elif self.type == "ac_3_voltage":
                self._state = report.ac_voltage[2]
            elif self.type == "ac_1_current":
                self._state = report.ac_current[0]
            elif self.type == "ac_2_current":
                self._state = report.ac_current[1]
            elif self.type == "ac_3_current":
                self._state = report.ac_current[2]
            elif self.type == "ac_1_power":
                self._state = report.ac_power[0]
            elif self.type == "ac_2_power":
                self._state = report.ac_power[1]
            elif self.type == "ac_3_power":
                self._state = report.ac_power[2]
            elif self.type == "status":
                self._state = report.status

class HassPiko(Entity):
    """Representation of a Piko inverter."""

    def __init__(self,  host, hass):
        """Initialize the data object."""
        self.piko = KostalPiko(ip_address=host)
        self.hass = hass
        self.report = None
        self.info = None
        self.async_info_update()

    @Throttle(MIN_TIME_BETWEEN_UPDATES)
    async def async_update(self):
        """Update inverter data."""
        # pylint: disable=protected-access
        self.report = await self.hass.async_add_executor_job(self.piko.report)
        _LOGGER.debug(self.report)

    async def async_info_update(self):
        """Update inverter info."""
        # pylint: disable=protected-access
        self.info = await self.hass.async_add_executor_job(self.piko.info)
        _LOGGER.debug(self.info)
