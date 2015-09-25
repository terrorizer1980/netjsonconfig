"""
OpenWrt specific JSON-Schema definition
"""
from .timezones import timezones
from ...schema import schema as default_schema
from ...utils import merge_dict

schema = merge_dict(default_schema, {
    "properties": {
        "general": {
            "properties": {
                "timezone": {
                    "id": "timezone",
                    "type": "string",
                    "default": "Coordinated Universal Time",
                    "enum": list(timezones.keys())
                }
            }
        },
        "radios": {
            "items": {
                "properties": {
                    "driver": {
                        "id": "driver",
                        "type": "string",
                        "enum": [
                            "mac80211",
                            "ath5k",
                            "ath9k",
                            "broadcom"
                        ]
                    },
                    "protocol": {
                        "id": "protocol",
                        "type": "string",
                        "enum": [
                            "802.11a",
                            "802.11b",
                            "802.11g",
                            "802.11n",
                            "802.11ac"
                        ]
                    }
                }
            }
        }
    },
    "ntp": {
        "id": "ntp",
        "type": "object",
        "title": "ntp settings",
        "additionalProperties": True,
        "properties": {
            "enabled": {
                "id": "enabled",
                "type": "boolean"
            },
            "enable_server": {
                "id": "enable_server",
                "type": "boolean"
            },
            "server": {
                "id": "server",
                "type": "array"
            }
        }
    },
    "ip_rules": {
        "id": "ip_rules",
        "type": "array",
        "title": "Ip rules",
        "uniqueItems": True,
        "additionalItems": False,
        "items": {
            "type": "object",
            "title": "Ip rule",
            "additionalProperties": True,
            "properties": {
                "in": {
                    "id": "in",
                    "type": "string"
                },
                "out": {
                    "id": "out",
                    "type": "string"
                },
                "src": {
                    "id": "src",
                    "type": "string"
                },
                "dest": {
                    "id": "dest",
                    "type": "string"
                },
                "tos": {
                    "id": "tos",
                    "type": "integer"
                },
                "mark": {
                    "id": "mark",
                    "type": "string"
                },
                "invert": {
                    "id": "invert",
                    "type": "boolean",
                    "default": False
                },
                "lookup": {
                    "id": "invert",
                    "type": "string"
                },
                "goto": {
                    "id": "goto",
                    "type": "integer"
                },
                "action": {
                    "id": "action",
                    "type": "string",
                    "enum": [
                        "prohibit",
                        "unreachable",
                        "blackhole",
                        "throw"
                    ]
                }
            }
        }
    }
})

# add interface protos
schema['properties']['interfaces']['items']['properties']\
      ['addresses']['items']['properties']['proto']['enum'] += [
    'dhcpv6',
    'ppp',
    'pppoe',
    'pppoa',
    '3g',
    'qmi',
    'ncm',
    'hnet',
    'pptp',
    '6in4',
    'aiccu',
    '6to4',
    '6rd',
    'dslite',
    'l2tp',
    'relay',
    'gre',
    'gretap',
    'grev6',
    'grev6tap'
]

# mark driver and protocol as required
schema['properties']['radios']['items']['required'] += [
    'driver',
    'protocol'
]
