"""Switch platform for IPMI Control integration."""
from __future__ import annotations

import logging
from typing import Any

from homeassistant.components.switch import SwitchEntity
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
    """Set up the IPMI switches."""
    ipmi_config = hass.data[DOMAIN][config_entry.entry_id]
    host = ipmi_config["host"]
    username = ipmi_config["username"]
    password = ipmi_config["password"]
    port = ipmi_config["port"]

    async_add_entities(
        [
            IPMIPowerSwitch(host, username, password, port, "Power Up", "power_up"),
            IPMIPowerSwitch(host, username, password, port, "Power Down", "power_down"),
            IPMIPowerSwitch(host, username, password, port, "Power Reset", "power_reset"),
        ]
    )


class IPMIPowerSwitch(SwitchEntity):
    """Representation of an IPMI Power Switch."""

    _attr_has_entity_name = True

    def __init__(self, host: str, username: str, password: str, port: int, name: str, command: str) -> None:
        """Initialize the switch."""
        self._host = host
        self._username = username
        self._password = password
        self._port = port
        self._attr_name = name
        self._command = command
        self._attr_unique_id = f"{host}_{command}"
        self._is_on = False  # L'état réel ne peut pas toujours être déterminé facilement via IPMI

    @property
    def is_on(self) -> bool | None:
        """Return the state of the switch."""
        return self._is_on

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn the entity on."""
        try:
            from ipmi import IPMIInterface

            interface = IPMIInterface(hostname=self._host, username=self._username, password=self._password, port=self._port)
            if self._command == "power_up":
                interface.set_power(True)
            elif self._command == "power_reset":
                interface.set_power(False)  # Certains systèmes nécessitent un arrêt avant le redémarrage
                await self.hass.async_add_executor_job(lambda: __import__('time').sleep(5)) # Attendre un peu
                interface.set_power(True)
            self._is_on = True  # On suppose que la commande a réussi
            interface.close()
            self.async_write_ha_state()
        except ImportError as e:
            _LOGGER.error(f"La librairie python-ipmi n'est pas installée: {e}")
        except Exception as e:
            _LOGGER.error(f"Erreur lors de l'envoi de la commande IPMI '{self._command}' à {self._host}: {e}")

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn the entity off."""
        try:
            from ipmi import IPMIInterface

            interface = IPMIInterface(hostname=self._host, username=self._username, password=self._password, port=self._port)
            if self._command == "power_down":
                interface.set_power(False)
            self._is_on = False  # On suppose que la commande a réussi
            interface.close()
            self.async_write_ha_state()
        except ImportError as e:
            _LOGGER.error(f"La librairie python-ipmi n'est pas installée: {e}")
        except Exception as e:
            _LOGGER.error(f"Erreur lors de l'envoi de la commande IPMI '{self._command}' à {self._host}: {e}")

    async def async_update(self) -> None:
        """Fetch new state data for the switch. (Optionnel, l'état réel est difficile à déterminer)"""
        pass