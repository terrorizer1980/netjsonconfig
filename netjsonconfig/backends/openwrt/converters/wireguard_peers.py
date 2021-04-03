from ..schema import schema
from .base import OpenWrtConverter


class WireguardPeers(OpenWrtConverter):
    netjson_key = 'wireguard_peers'
    intermediate_key = 'network'
    _schema = schema['properties']['wireguard_peers']['items']
    # unfortunately due to the design of the
    # wireguard OpenWRT package, this is unpredictable
    _uci_types = None

    def to_intermediate_loop(self, block, result, index=None):
        result.setdefault('network', [])
        result['network'].append(self.__intermediate_peer(block))
        return result

    def __intermediate_peer(self, peer):
        interface = peer.pop("interface")
        peer.update({'.type': f'wireguard_{interface}', '.name': 'wgpeer'})
        if not peer.get('endpoint_host') and 'endpoint_port' in peer:
            del peer['endpoint_port']
        return self.sorted_dict(peer)

    def to_netjson_loop(self, block, result, index):
        result.setdefault('wireguard_peers', [])
        result['wireguard_peers'].append(self.__netjson_peer(block))
        return result

    def __netjson_peer(self, peer):
        del peer['.name']
        interface = peer.pop('.type').replace('wireguard_', '')
        peer['interface'] = interface
        return self.type_cast(peer)
