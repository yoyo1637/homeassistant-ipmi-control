"""Sensor platform for IPMI Control integration."""
from __future__ import annotations

import logging
from typing import Any

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the IPMI sensors."""
    ipmi_config = hass.data[DOMAIN][config_entry.entry_id]
    host = ipmi_config["host"]
    username = ipmi_config["username"]
    password = ipmi_config["password"]
    port = ipmi_config["port"]

    sensors = []

    # Exemple de récupération de la consommation électrique
    try:
        from ipmi import IPMIInterface

        interface = IPMIInterface(hostname=host, username=username, password=password, port=port)
        power_reading = interface.get_power_reading()
        if power_reading:
            sensors.append(IPMIPowerSensor(host, power_reading, config_entry.entry_id, hass))

        # Exemple de récupération de la température (Adaptez le nom du capteur)
        temperature_reading = interface.get_sensor_reading("Ambient Temp")
        if temperature_reading is not None:
            sensors.append(IPMITemperatureSensor(host, temperature_reading, config_entry.entry_id, hass))

        interface.close()
    except ImportError as e:
        _LOGGER.error(f"La librairie python-ipmi n'est pas installée: {e}")
    except Exception as e:
        _LOGGER.error(f"Erreur lors de la récupération des données IPMI de {host}: {e}")

    async_add_entities(sensors)


class IPMIPowerSensor(SensorEntity):
    """Representation of an IPMI Power Sensor."""

    _attr_native_unit_of_measurement = "W"
    _attr_device_class = "power"
    _attr_state_class = "measurement"
    _attr_has_entity_name = True

    def __init__(self, host: str, initial_value: Any, config_entry_id: str, hass: HomeAssistant) -> None:
        """Initialize the sensor."""
        self._attr_name = "Power Consumption"
        self._attr_unique_id = f"{host}_power_consumption"
        self._state = initial_value
        self._host = host
        self._username = None
        self._password = None
        self._port = None
        self.config_entry_id = config_entry_id
        self.hass = hass
        self._update_interval = 60
        self._last_update = None

    @property
    def native_value(self) -> Any:
        """Return the state of the sensor."""
        return self._state

    async def async_update(self) -> None:
        """Fetch new state data for the sensor."""
        import time
        if self._last_update is not None and time.time() - self._last_update < self._update_interval:
            return

        try:
            from ipmi import IPMIInterface

            ipmi_config = self.hass.data[DOMAIN].get(self.config_entry_id)
            if ipmi_config:
                self._host = ipmi_config["host"]
                self._username = ipmi_config["username"]
                self._password = ipmi_config["password"]
                self._port = ipmi_config["port"]

                interface = IPMIInterface(hostname=self._host, username=self._username, password=self._password, port=self._port)
                power_reading = interface.get_power_reading()
                if power_reading is not None:
                    self._state = power_reading
                interface.close()
                self._last_update = time.time()
        except Exception as e:
            _LOGGER.error(f"Erreur lors de la mise à jour des données IPMI de {self._attr_name} ({self._host}): {e}")


class IPMITemperatureSensor(SensorEntity):
    """Representation of an IPMI Temperature Sensor."""

    _attr_native_unit_of_measurement = "°C"
    _attr_device_class = "temperature"
    _attr_state_class = "measurement"
    _attr_has_entity_name = True

    def __init__(self, host: str, initial_value: Any, config_entry_id: str, hass: HomeAssistant) -> None:
        """Initialize the sensor."""
        self._attr_name = "Temperature"
        self._attr_unique_id = f"{host}_temperature"
        self._state = initial_value
        self._host = host
        self._username = None
        self._password = None
        self._port = None
        self.config_entry_id = config_entry_id
        self._update_interval = 60
        self._last_update = None
        self.hass = hass

    @property
    def native_value(self) -> Any:
        """Return the state of the sensor."""
        return self._state

    async def async_update(self) -> None:
        """Fetch new state data for the temperature sensor."""
        import time
        if self._last_update is not None and time.time() - self._last_update < self._update_interval:
            return

        try:
            from ipmi import IPMIInterface

            ipmi_config = self.hass.data[DOMAIN].get(self.config_entry_id)
            if ipmi_config:
                self._host = ipmi_config["host"]
                self._username = ipmi_config["username"]
                self._password = ipmi_config["password"]
                self._port = ipmi_config["port"]

                interface = IPMIInterface(hostname=self._host, username=self._username, password=self._password, port=self._port)
                temperature_reading = interface.get_sensor_reading("Ambient Temp")  # Adaptez le nom du capteur ici
                if temperature_reading is not None:
                    self._state = temperature_reading
                interface.close()
                self._last_update = time.time()
        except Exception as e:
            _LOGGER.error(f"Erreur lors de la mise à jour de la température IPMI de {self._host}: {e}")