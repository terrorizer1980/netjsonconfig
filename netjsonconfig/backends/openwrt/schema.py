"""
OpenWrt specific JSON-Schema definition
"""
from ...schema import schema as default_schema
from ...utils import merge_config
from ..openvpn.schema import base_openvpn_schema
from .timezones import timezones

default_radio_driver = "mac80211"
_interface_properties = default_schema["definitions"]["interface_settings"][
    "properties"
]


schema = merge_config(
    default_schema,
    {
        "definitions": {
            "interface_settings": {
                "properties": {
                    "network": {
                        "type": "string",
                        "description": "logical interface name in UCI (OpenWRT configuration format), "
                        "will be automatically generated if left blank",
                        "maxLength": 15,
                        "pattern": "^[a-zA-z0-9_\\.\\-]*$",
                        "propertyOrder": 7,
                    }
                }
            },
            "wireless_interface": {
                "properties": {
                    "wireless": {
                        "properties": {
                            "network": {
                                "type": "array",
                                "title": "Attached Networks",
                                "description": "override OpenWRT \"network\" config option of of wifi-iface "
                                "directive; will be automatically determined if left blank",
                                "uniqueItems": True,
                                "additionalItems": True,
                                "items": {
                                    "title": "network",
                                    "type": "string",
                                    "$ref": "#/definitions/interface_settings/properties/network",
                                },
                                "propertyOrder": 19,
                            }
                        }
                    }
                }
            },
            "ap_wireless_settings": {
                "allOf": [
                    {
                        "properties": {
                            "wmm": {
                                "type": "boolean",
                                "title": "WMM (802.11e)",
                                "description": "enables WMM (802.11e) support; "
                                "required for 802.11n support",
                                "default": True,
                                "format": "checkbox",
                                "propertyOrder": 8,
                            },
                            "isolate": {
                                "type": "boolean",
                                "title": "isolate clients",
                                "description": "isolate wireless clients from one another",
                                "default": False,
                                "format": "checkbox",
                                "propertyOrder": 9,
                            },
                            "macfilter": {
                                "type": "string",
                                "title": "MAC Filter",
                                "description": "specifies the mac filter policy, \"disable\" to disable "
                                "the filter, \"allow\" to treat it as whitelist or "
                                "\"deny\" to treat it as blacklist",
                                "enum": ["disable", "allow", "deny"],
                                "default": "disable",
                                "propertyOrder": 15,
                            },
                            "maclist": {
                                "type": "array",
                                "title": "MAC List",
                                "description": "mac addresses that will be filtered according to the policy "
                                "specified in the \"macfilter\" option",
                                "propertyOrder": 16,
                                "items": {
                                    "type": "string",
                                    "title": "MAC address",
                                    "pattern": "^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$",
                                    "minLength": 17,
                                    "maxLength": 17,
                                },
                            },
                        }
                    }
                ]
            },
            "bridge_interface": {
                "allOf": [
                    {
                        "properties": {
                            "igmp_snooping": {
                                "type": "boolean",
                                "title": "IGMP snooping",
                                "description": "sets the \"multicast_snooping\" kernel setting for a bridge",
                                "default": True,
                                "format": "checkbox",
                                "propertyOrder": 4,
                            }
                        }
                    }
                ]
            },
            "dialup_interface": {
                "title": "Dialup interface",
                "required": ["proto", "username", "password"],
                "allOf": [
                    {
                        "properties": {
                            "type": {
                                "type": "string",
                                "enum": ["dialup"],
                                "default": "dialup",
                                "propertyOrder": 1,
                            },
                            "proto": {
                                "type": "string",
                                "title": "protocol",
                                "enum": [
                                    "3g",
                                    "6in4",
                                    "aiccu",
                                    "l2tp",
                                    "ncm",
                                    "ppp",
                                    "pppoa",
                                    "pppoe",
                                    "pptp",
                                    "qmi",
                                    "wwan",
                                ],
                                "default": "pppoe",
                                "propertyOrder": 1.1,
                            },
                            "username": {
                                "type": "string",
                                "description": "username for authentication in protocols like PPPoE",
                                "propertyOrder": 9,
                            },
                            "password": {
                                "type": "string",
                                "description": "password for authentication in protocols like PPPoE",
                                "propertyOrder": 10,
                            },
                        }
                    },
                    {"$ref": "#/definitions/interface_settings"},
                ],
            },
            "modemmanager_interface": {
                "type": "object",
                "title": "Modem manager interface",
                "required": ["name", "device"],
                "properties": {
                    "name": _interface_properties["name"],
                    "mtu": _interface_properties["mtu"],
                    "autostart": _interface_properties["autostart"],
                    "disabled": _interface_properties["disabled"],
                    "type": {
                        "type": "string",
                        "enum": ["modem-manager"],
                        "default": "dialup",
                        "propertyOrder": 1,
                    },
                    "apn": {"type": "string", "title": "APN", "propertyOrder": 1.1},
                    "pin": {
                        "type": "string",
                        "title": "PIN code",
                        "propertyOrder": 1.2,
                    },
                    "device": {
                        "type": "string",
                        "description": "Leave blank to use the hardware default",
                        "propertyOrder": 1.3,
                    },
                    "username": {"type": "string", "propertyOrder": 1.4},
                    "password": {"type": "string", "propertyOrder": 1.5},
                    "metric": {"type": "integer", "default": 50, "propertyOrder": 1.6},
                    "iptype": {
                        "type": "string",
                        "title": "IP type",
                        "default": "ipv4",
                        "enum": ["ipv4", "ipv6", "ipv4v6"],
                        "options": {"enum_titles": ["IPv4", "IPv6", "IPv4 and IPv6"]},
                        "propertyOrder": 1.7,
                    },
                    "lowpower": {
                        "type": "boolean",
                        "title": "Low power mode",
                        "format": "checkbox",
                        "default": False,
                        "propertyOrder": 1.8,
                    },
                },
            },
            "base_radio_settings": {
                "properties": {
                    "driver": {
                        "type": "string",
                        "enum": ["mac80211", "atheros", "ath5k", "ath9k", "broadcom"],
                        "default": default_radio_driver,
                        "propertyOrder": 2,
                    }
                }
            },
            "radio_hwmode_11g": {
                "properties": {
                    "hwmode": {
                        "type": "string",
                        "title": "hardware mode",
                        "readOnly": True,
                        "propertyOrder": 8,
                        "default": "11g",
                        "enum": ["11g"],
                    }
                }
            },
            "radio_hwmode_11a": {
                "properties": {
                    "hwmode": {
                        "type": "string",
                        "title": "hardware mode",
                        "readOnly": True,
                        "propertyOrder": 8,
                        "default": "11a",
                        "enum": ["11a"],
                    }
                }
            },
            "radio_80211gn_settings": {
                "allOf": [{"$ref": "#/definitions/radio_hwmode_11g"}]
            },
            "radio_80211an_settings": {
                "allOf": [{"$ref": "#/definitions/radio_hwmode_11a"}]
            },
            "radio_80211ac_2ghz_settings": {
                "allOf": [{"$ref": "#/definitions/radio_hwmode_11g"}]
            },
            "radio_80211ac_5ghz_settings": {
                "allOf": [{"$ref": "#/definitions/radio_hwmode_11a"}]
            },
        },
        "properties": {
            "general": {
                "properties": {
                    "timezone": {"enum": list(timezones.keys()), "default": "UTC"}
                }
            },
            "interfaces": {
                "items": {
                    "oneOf": [
                        {"$ref": "#/definitions/dialup_interface"},
                        {"$ref": "#/definitions/modemmanager_interface"},
                    ]
                }
            },
            "routes": {
                "items": {
                    "properties": {
                        "type": {
                            "type": "string",
                            "enum": [
                                "unicast",
                                "local",
                                "broadcast",
                                "multicast",
                                "unreachable",
                                "prohibit",
                                "blackhole",
                                "anycast",
                            ],
                            "default": "unicast",
                            "propertyOrder": 0,
                        },
                        "mtu": {
                            "type": "string",
                            "title": "MTU",
                            "propertyOrder": 6,
                            "pattern": "^[0-9]*$",
                        },
                        "table": {
                            "type": "string",
                            "propertyOrder": 7,
                            "pattern": "^[0-9]*$",
                        },
                        "onlink": {
                            "type": "boolean",
                            "default": False,
                            "format": "checkbox",
                            "propertyOrder": 8,
                        },
                    }
                }
            },
            "ip_rules": {
                "type": "array",
                "title": "Policy routing",
                "uniqueItems": True,
                "additionalItems": True,
                "propertyOrder": 7,
                "items": {
                    "type": "object",
                    "title": "IP rule",
                    "additionalProperties": True,
                    "properties": {
                        "in": {
                            "type": "string",
                            "title": "incoming interface",
                            "propertyOrder": 1,
                        },
                        "out": {
                            "type": "string",
                            "title": "outgoing interface",
                            "propertyOrder": 2,
                        },
                        "src": {
                            "type": "string",
                            "title": "source subnet",
                            "description": "(CIDR notation)",
                            "propertyOrder": 3,
                            "format": "cidr",
                        },
                        "dest": {
                            "type": "string",
                            "title": "destination subnet",
                            "description": "(CIDR notation)",
                            "propertyOrder": 4,
                            "format": "cidr",
                        },
                        "tos": {
                            "type": "integer",
                            "title": "TOS",
                            "description": "TOS value to match in IP headers",
                            "propertyOrder": 5,
                        },
                        "mark": {
                            "type": "string",
                            "description": "TOS value to match in IP headers",
                            "propertyOrder": 6,
                        },
                        "lookup": {
                            "type": "string",
                            "description": "routing table ID or symbolic link alias",
                            "propertyOrder": 7,
                        },
                        "action": {
                            "type": "string",
                            "enum": ["prohibit", "unreachable", "blackhole", "throw"],
                            "propertyOrder": 8,
                        },
                        "goto": {"type": "integer", "propertyOrder": 9},
                        "invert": {
                            "type": "boolean",
                            "default": False,
                            "format": "checkbox",
                            "propertyOrder": 10,
                        },
                    },
                },
            },
            "ntp": {
                "type": "object",
                "title": "NTP Settings",
                "additionalProperties": True,
                "propertyOrder": 8,
                "properties": {
                    "enabled": {
                        "type": "boolean",
                        "title": "enable NTP client",
                        "default": True,
                        "format": "checkbox",
                        "propertyOrder": 1,
                    },
                    "enable_server": {
                        "type": "boolean",
                        "title": "enable NTP server",
                        "default": False,
                        "format": "checkbox",
                        "propertyOrder": 2,
                    },
                    "server": {
                        "title": "NTP Servers",
                        "description": "NTP server candidates",
                        "type": "array",
                        "uniqueItems": True,
                        "additionalItems": True,
                        "propertyOrder": 3,
                        "items": {
                            "title": "NTP server",
                            "type": "string",
                            "format": "hostname",
                        },
                        "default": [
                            "0.openwrt.pool.ntp.org",
                            "1.openwrt.pool.ntp.org",
                            "2.openwrt.pool.ntp.org",
                            "3.openwrt.pool.ntp.org",
                        ],
                    },
                },
            },
            "switch": {
                "type": "array",
                "uniqueItems": True,
                "additionalItems": True,
                "title": "Programmable Switch",
                "propertyOrder": 9,
                "items": {
                    "title": "Switch",
                    "type": "object",
                    "additionalProperties": True,
                    "required": ["name", "reset", "enable_vlan", "vlan"],
                    "properties": {
                        "name": {"type": "string", "propertyOrder": 1},
                        "reset": {
                            "type": "boolean",
                            "default": True,
                            "format": "checkbox",
                            "propertyOrder": 2,
                        },
                        "enable_vlan": {
                            "type": "boolean",
                            "title": "enable vlan",
                            "default": True,
                            "format": "checkbox",
                            "propertyOrder": 3,
                        },
                        "vlan": {
                            "type": "array",
                            "title": "VLANs",
                            "uniqueItems": True,
                            "additionalItems": True,
                            "propertyOrder": 4,
                            "items": {
                                "type": "object",
                                "title": "VLAN",
                                "additionalProperties": True,
                                "required": ["device", "vlan", "ports"],
                                "properties": {
                                    "device": {"type": "string", "propertyOrder": 1},
                                    "vlan": {"type": "integer", "propertyOrder": 2},
                                    "ports": {"type": "string", "propertyOrder": 3},
                                },
                            },
                        },
                    },
                },
            },
            "led": {
                "type": "array",
                "title": "LEDs",
                "uniqueItems": True,
                "additionalItems": True,
                "propertyOrder": 10,
                "items": {
                    "type": "object",
                    "title": "LED",
                    "additionalProperties": True,
                    "required": ["name", "sysfs", "trigger"],
                    "properties": {
                        "name": {"type": "string", "propertyOrder": 1},
                        "default": {
                            "type": "boolean",
                            "format": "checkbox",
                            "propertyOrder": 2,
                        },
                        "dev": {"type": "string", "propertyOrder": 3},
                        "sysfs": {"type": "string", "propertyOrder": 4},
                        "trigger": {"type": "string", "propertyOrder": 5},
                        "delayoff": {"type": "integer", "propertyOrder": 6},
                        "delayon": {"type": "integer", "propertyOrder": 7},
                        "interval": {"type": "integer", "propertyOrder": 8},
                        "message": {"type": "string", "propertyOrder": 9},
                        "mode": {"type": "string", "propertyOrder": 10},
                    },
                },
            },
        },
    },
)

# add OpenVPN schema
schema = merge_config(schema, base_openvpn_schema)
# OpenVPN customizations for OpenWRT
schema = merge_config(
    schema,
    {
        "definitions": {
            "tunnel": {
                "properties": {
                    "disabled": {
                        "title": "disabled",
                        "description": "disable this VPN without deleting its configuration",
                        "type": "boolean",
                        "default": False,
                        "format": "checkbox",
                        "propertyOrder": 1,
                    }
                }
            }
        }
    },
)
