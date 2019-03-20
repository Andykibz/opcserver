from snap7.client import Client as PlcClient
from opcua import Client
from index.models import Server
from snap7.snap7types import areas
from snap7 import util
import time
import threading
from random import randint
import socket
# import logging
# logging.basicConfig(level=logging.DEBUG)
# loggger = logging.getLogger()


class MyPlc:
    instantiated = 0
    def __init__(self,server_id, ip='192.168.0.1'):
        self.db_server = Server.query.get( server_id )
        self.plc = PlcClient()
        self.ip = ip
        self.ep_url = 'opc.tcp://'+self.db_server.endpoint_url
        self.opc_ns_uri = self.db_server.namespace
        self.opclient = Client(self.ep_url)
        self.INByteArray = bytearray([ 0, 0 ])
        self.threadStatus = False
        self.varsdict = {}
        self.threads={}
        self.connections()
        self.areas={ 'I' : 0x81, 'O' : 0x82, 'M' : 0x83 }
        instantiated += 1
        

    def connections( self ):
        # self.plc.connect( self.ip, 0, 1 )
        self.opclient.connect()
        self.root = self.opclient.get_root_node()
        self.idx = self.opclient.get_namespace_index(self.db_server.namespace)
        self.set_tags(self.db_server.objects)
        self.run_threads()

    def set_tags(self,objs):
        for obj in objs:
            self.make_tag_dict(obj, obj.variables)
            
    def make_tag_dict(self,obj,allvars):
        for var in allvars:
            self.varsdict[var.tag_id] = {
                'obj'   :self.root.get_child( [ "0:Objects", "{}:{}".format(self.idx,obj.name), "{}:{}".format(self.idx,var.name) ] ),
                'type'  : var.type
            }
    def kill_threads(self):
        self.threadStatus = False
        
    def run_threads(self):
        self.threadStatus = True
        self.threads['inputs'] = threading.Thread( target=self.getInputs )
        self.threads['update_server'] = threading.Thread( target=self.updateInputs )
        # threads['merkels'] = threading.Thread( target=getMerkels, args() )
        # threads['outputs'] = threading.Thread( target=getOutputs, args() )
        self.threads['inputs'].start()
        self.threads['update_server'].start()

    def getInputs( self ):
        while self.threadStatus:
            # self.INByteArray = self.plc.read_area( areas['PE'], 0, 0, 2 )
            self.INByteArray = bytearray([ randint(0,7), randint(0,7) ])
            time.sleep(.5)

    # def get_bool(_bytearray, byte_index, bool_index):
    def updateInputs(self):
        while True:
            for key,val in self.varsdict.items():
                if val['type'] == 'bool':
                    bit = int( key.split('.')[1] )
                    byt = int( key.split('.')[0][1:] )
                    util.get_bool( self.INByteArray, byt, bit )
                    val['obj'].set_value( util.get_bool( self.INByteArray, byt, bit ) )
        time.sleep(.5)

    def show_tags(self):
        for key,val in self.varsdict.items():
            print(val['obj'].get_value())

     

    
         

