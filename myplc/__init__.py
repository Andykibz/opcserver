from snap7.client import Client as PlcClient
from opcua import Client
from index.models import Server
from snap7.snap7types import areas
from snap7.util import *
import time
import threading
from random import randint
import socket
# import logging
# logging.basicConfig(level=logging.DEBUG)
# loggger = logging.getLogger()



class MyPlc:
    area={ 'I' : 0x81, 'Q' : 0x82, 'M' : 0x83, 'D': 0x84 }
    szs = { 'x':1, 'X': 1, 'b':1, 'B':1, 'w' : 2, 'W' : 2, 'd' : 4, 'D' : 4 }
    
    def __init__(self, ip='192.168.0.1'):
        self.ip = ip
        self.INByteArray = bytearray([ 0, 0 ])
        self.MKByteArray = bytearray([ 0, 0 ])
        self.threadStatus = False
        self.varsdict = {}
        self.threads={}
        self.plc = PlcClient()
        


    def get_db(self,server_id):        
        self.db_server = Server.query.get( server_id )
        self.connections()


    def connections( self ):        
        self.opc_ns_uri = self.db_server.server_namespace
        self.ep_url = 'opc.tcp://'+self.db_server.server_endpoint_url
        self.opclient = Client(self.ep_url)
        try:
            self.plc.connect( self.ip, 0, 1 )
            # pass
        except Exception:
            self.conn_stat = "Could not connect to PLC"
        else:
            self.conn_stat = "PLC Connected Successfully"
            
        self.opclient.connect()
        self.root = self.opclient.get_root_node()
        self.idx = self.opclient.get_namespace_index(self.db_server.server_namespace)
        self.set_tags(self.db_server.server_objects)
        self.run_threads()
        handler = SubHandler()
        sub = self.opclient.create_subscription(200, handler)
        handle = sub.subscribe_data_change(self.varsdict['M0.0']['obj'])
        time.sleep(0.1)

    def set_tags(self,objs):
        for obj in objs:
            try:
                self.make_tag_dict(obj, obj.object_variables)
            except Exception:
                self.make_tags_dict(obj.object_variables)
            
    def make_tag_dict(self,obj,allvars):
        for var in allvars:
            self.varsdict[var.variable_address] = {
                'obj'   :self.root.get_child( [ "0:Objects", "{}:{}".format(self.idx,obj.object_name), "{}:{}".format(self.idx,var.variable_name) ] ),
                'type'  : var.variable_type
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
        while self.threadStatus:
            for key,val in self.varsdict.items():
                self.update_server_vars(key)
                # if val['type'] == 'bool':
                #     bit = int( key.split('.')[1] )
                #     byt = int( key.split('.')[0][1:] )
                #     if split('.')[0][:1] is 'I':
                #         util.get_bool( self.INByteArray, byt, bit )
                #         val['obj'].set_value( get_bool( self.INByteArray, byt, bit ) )                        
                time.sleep(.1)                        
    
    '''
        Get Data from the PLC and Update OPC Server variables
    '''
    def update_server_vars(self, addr_key ):
        addr = addr_key.split('.')
        # Works with Boolean values from a Data Block
        if len(addr) == 3 and addr[0][0] == 'D':
            DBn = int(addr[0][2:])
            DBt = addr[1][2]
            byt = int( addr[1][3:] )
            bit = int( addr[2] )
            reading = self.plc.read_area( MyPlc.area['D'], DBn, byt, szs[DBt] )
            if DBt == 'X' or DBt == 'x':
                self.varsdict[addr_key]['obj'].set_value( get_bool( reading, 0, bit ) )
                # return get_bool( reading, 0, bit )
            else:
                self.varsdict[addr_key]['obj'].set_value( reading )
                # return reading 
           
        # Works with other data types from a Data Block
        elif len(addr) == 2 and addr[0][0] == 'D':
            DBn = int(addr[0][2:])
            DBt = addr[1][2]
            byt = int( addr[1][3:] )
            reading = self.plc.read_area( MyPlc.area['D'], DBn, byt, szs[DBt] )
            if DBt == 'W' or DBt == 'w':
                self.varsdict[addr_key]['obj'].set_value( get_int(reading,0) )
                # return get_int(reading,0)
            elif DBt == 'D' or DBt == 'd':
                self.varsdict[addr_key]['obj'].set_value( get_real(reading,0) )
                # return get_real(reading,0)
            else:
                self.varsdict[addr_key]['obj'].set_value( reading )

        # Works with boolean values from Inputs,Merkels ot Outputs
        elif len(addr) == 2 :        
            byt = int( addr[0][1:] )
            bit = int( addr[1] )
            reading = self.plc.read_area( MyPlc.area[addr[0][0]], 0, byt, 1 )
            self.varsdict[addr_key]['obj'].set_value( get_bool(reading,0,bit) )
            # return get_bool(reading,0,bit)    

        # Works with other data types from Inputs,Merkels ot Outputs eg MW2
        elif len(addr) == 1:
            byt = int( addr[0][2:] )
            typ =  addr[0][1]
            reading =  self.plc.read_area( MyPlc.area[ addr[0][0] ], 0, byt, 2 )        
            if typ == 'w' or typ == 'W':
                self.varsdict[addr_key]['obj'].set_value( get_int(reading,0) )
                # return get_int(reading, 0)
            elif typ == 'd' or typ == 'D':
                self.varsdict[addr_key]['obj'].set_value( get_real(reading,0) )
                # return get_real(reading, 0)
            else:
                self.varsdict[addr_key]['obj'].set_value( reading )
                # return reading

    '''
        WRITE DATA TO PLC
    '''
    def write_to_plc(self, addr_key, value ):
        addr = addr_key.split('.')
        
        # Works with Boolean values from a Data Block
        if len(addr) == 3 and addr[0][0] == 'D':
            DBn = int(addr[0][2:])
            DBt = addr[1][2]
            byt = int( addr[1][3:] )
            bit = int( addr[2] )
            reading = self.plc.read_area( MyPlc.area['D'], DBn, byt, szs[DBt] )
            if DBt == 'X' or DBt == 'x':
                set_bool(reading, 0, bit, value)   
            self.plc.write_area( MyPlc.area['D'], DBn, byt, reading )

        # Works with other data types from a Data Block
        elif len(addr) == 2 and addr[0][0] == 'D':
            DBn = int(addr[0][2:])
            DBt = addr[1][2]
            byt = int( addr[1][3:] )
            reading = self.plc.read_area( MyPlc.area['D'], DBn, byt, szs[DBt] )
            if DBt == 'W' or DBt == 'w':
                set_int(reading, 0, value)
            elif DBt == 'D' or DBt == 'd':
                set_real(reading, 0, value)                
            self.plc.write_area( MyPlc.area['D'], DBn, byt, reading )
            
        # Works with boolean values from Inputs,Merkels ot Outputs
        elif len(addr) == 2 :        
            byt = int( addr[0][1:] )
            bit = int( addr[1] )
            reading = plc.read_area( MyPlc.area[addr[0][0]], 0, byt, 1 )
            set_bool(reading, 0, bit, value) 
            self.plc.write_area( MyPlc.area[addr[0][0]], 0, byt, reading )
            
        # Works with other data types from Inputs,Merkels ot Outputs eg MW2
        elif len(addr) == 1:
            byt = int( addr[0][2:] )
            typ =  addr[0][1]
            reading =  self.plc.read_area( MyPlc.area[ addr[0][0] ], 0, byt, 2 )
            if typ == 'w' or typ == 'W':
                set_int(reading, 0, value)
            elif typ == 'd' or typ == 'D':
                set_real(reading, 0, value)
            else:
                set_data( value )
            self.plc.write_area( MyPlc.area[addr[0][0]], 0, byt, reading )

     
class SubHandler(MyPlc):

    """
    Subscription Handler. To receive events from server for a subscription
    data_change and event methods are called directly from receiving thread.
    Do not do expensive, slow or network operation there. Create another 
    thread if you need to do such a thing
    """

    def datachange_notification(self, node, val, data):
        self.threads['writetoplc'] = threading.Thread( args=(val,node) , target=self.writetoPLC)
        self.threads['writetoplc'].start()
        print("Python: New data change event", node, val)

    def event_notification(self, event):
        print("Python: New event", event)

    def writetoPLC(self,value,node):
        for key,val in self.varsdict.items():
            if val['obj'] is node:
                self.write_to_plc( key, value )
            #     byt = key.split('.')[0][1:]
            #     bit = key.split('.')
            #     bArray = self.plc.read_area(areas['MK'],0,byt+1,1)
            #     set_bool( bArray, byt, bit, value)
            #     self.plc.write_area(['MK'],0,byt+1,bArray)
            #          
                


