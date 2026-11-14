"""Constants for the AtGlance Dashboard integration."""

from __future__ import annotations

DOMAIN = "atglance"
VERSION = "1.0.0"

PANEL_URL = "atglance"
STATIC_URL = "/atglance_static"

STORAGE_KEY = "atglance.config"
STORAGE_VERSION = 1

CONF_SIDEBAR_TITLE = "sidebar_title"
CONF_SIDEBAR_ICON = "sidebar_icon"
CONF_REQUIRE_ADMIN = "require_admin"
CONF_MIGRATE_LOVELACE = "migrate_lovelace"
CONF_DEFAULT_DASHBOARD = "default_dashboard"

DEFAULT_SIDEBAR_TITLE = "AtGlance"
DEFAULT_SIDEBAR_ICON = "mdi:view-dashboard-outline"
DEFAULT_SET_DEFAULT_DASHBOARD = True

LEGACY_LOVELACE_DASHBOARD = "vision-glass"
LEGACY_STORAGE_KEYS = ("vision_glass.config", "lovelace.vision_glass", "lovelace.vision-glass")

DEFAULT_CONFIG: dict = {
    "_initialized": False,
    "default_dashboard": True,
    "theme_mode": "auto",
    "background_style": "aurora",
    "ambient_speed": "normal",
    "background_mode": "mesh",
    "color_scheme": "default",
    "dashboard_title": "Smart Home",
    "weather_entity": None,
    "lock_entity": None,
    "all_lights_entity": None,
    "rooms": [],
    "bento_badges": [],
    "top_badges": [],
    "helper_controls": {},
    "stats": {
        "rooms": {},
        "show_temperature": True,
        "show_illuminance": True,
        "show_battery": True,
        "custom_sections": [],
    },
    "dock": {
        "auto_detect": True,
        "items": [],
    },
}
