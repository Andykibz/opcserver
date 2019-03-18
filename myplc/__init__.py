from snap7.client import PlcClient
from opcua import Client
from index.models import Server


class Snap_Cl:
    __init__(server_id, ip='198.168.0.50'):
        self.db_server = Server.query.get( server_id )
        self.plc = PlcClient.Client()
        self.ep_url = self.db_server.endpoint_url
        self.opc_ns_uri = self.db_server.namespace
        self.connections()

    def connections( self ):
        self.plc.connect( self.ip, 0, 1 )
        self.opclient = Client(self.ep_url)
        self.root = opclient.get_root_node()

    def read_tags():
        pass