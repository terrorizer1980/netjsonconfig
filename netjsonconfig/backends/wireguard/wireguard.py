from ..base.backend import BaseVpnBackend
from . import converters
from .parser import config_suffix, vpn_pattern
from .renderer import WireguardRenderer
from .schema import schema


class Wireguard(BaseVpnBackend):
    schema = schema
    converters = [converters.Wireguard]
    renderer = WireguardRenderer
    # BaseVpnBackend attributes
    vpn_pattern = vpn_pattern
    config_suffix = config_suffix

    @classmethod
    def auto_client(cls, host=None, pub_key=None, server={}, port=51820, **kwargs):
        """
        Returns a configuration dictionary representing Wireguard configuration
        that is compatible with the passed server configuration.

        :param host: remote VPN server
        :param port: listen port for Wireguard Client
        :param server: dictionary representing a single Wireguard server configuration
        :param pub_key: publick key of the Wireguard server
        :returns: dictionary representing a Wireguard server and client properties
        """
        server_name = server.get('name')
        return {
            'client': {
                'port': port,
                'private_key': '{{private_key}}',
                'name': f'{server_name}_client',
            },
            'server': {
                'name': server_name,
                'public_key': pub_key,
                'endpoint_host': host,
                'endpoint_port': server.get('port'),
                'allowed_ips': [kwargs.get('server_ip_max_prefix')],
            },
        }
