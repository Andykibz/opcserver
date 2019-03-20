from opcua import Server as UAServer
from index.models import Server,Object,Variable
from index.utils import convert_val

class MyServer:    
    '''
        initialise opcua server object
    '''
    addrs = []
    def __init__( self, server_id ):
        self.opc_server = UAServer()  # OPC UA server instance
        self.opc_objects_dict = {}
        self.opc_variables_dict = {}
        self.db_server=Server.query.get( server_id )
        self.initialise()
        self.addrs.append( self.db_server.endpoint_url )

    '''
     Instantiate all server related variables from the Sqlite DB server 
     to the opcua server instance
    '''
    def initialise( self  ):
        self.instantiate_server_vars()


    def instantiate_server_vars( self ):
        self.opc_server_endpoint = "opc.tcp://"+self.db_server.endpoint_url
        self.opc_server_name = self.db_server.name
        self.opc_server_uri = self.db_server.namespace
        self.ns_idx = self.opc_server.register_namespace( self.opc_server_uri )
        self.opc_objects = self.opc_server.get_objects_node()
        self.opc_server.set_endpoint(self.opc_server_endpoint)
        self.load_server( self.db_server.objects )

    '''
        load opc server with objects and variables from the SQlite DB
    '''
    def load_server( self, db_objects, parent_obj=None ):
        for server_obj in db_objects:
            if( server_obj.id not in self.opc_objects_dict ):
                if parent_obj is None:
                    self.opc_objects_dict[server_obj.id] = self.opc_objects.add_object( self.ns_idx, server_obj.name )
                else:
                    self.opc_objects_dict[server_obj.id] = parent_obj.add_object( self.ns_idx, server_obj.name )               

                self.load_object_variables(server_obj.variables, self.opc_objects_dict[server_obj.id])

                if( server_obj.get_child_objects().count() > 0 ):
                    self.load_server(server_obj.get_child_objects(),self.opc_objects_dict[server_obj.id] )


    def load_object_variables(self, variables, object_owner):
        for variable in variables:
            self.opc_variables_dict[variable.id] = object_owner.add_variable( self.ns_idx, variable.name, convert_val(variable.value,variable.type ) )
            if variable.writable:
                self.opc_variables_dict[variable.id].set_writable()

    def start_opc_server(self):
        self.opc_server.start()

    def stop_opc_server(self):
        self.opc_server.stop() 

    @classmethod
    def kill_all_servers(cls):
        for addr in addrs:
            pass
            
            
            
            

