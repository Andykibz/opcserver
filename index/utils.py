import socket
types = {
    "int"
}

def custom_validation(form):
    status = True
    for k,v in form.items():
        if v is None:
            status = False
    return status

def selectVals(objs):
    idlist = []
    namelist = []
    if objs:
        for obj in objs:
            idlist.append(obj.id)
            namelist.append(obj.object_name)
        return [(None,'Object')]+list(zip( idlist, namelist ))
    else:
        return [ (None, 'No Objects Defined' ) ]

def convert_val(val,vtype):
    if vtype is 'int':
        return int(val)
    elif vtype == 'float':        
        return float(val)
    elif vtype == 'string':        
        return str(val)
    elif vtype == 'bool':        
        if val == True or val == 'true' or val == 1:
            return True
        else:
            return False
    else:
        return val            



def isOpen( ep_url ):
   s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   try:
      s.connect( ( ep_url.split(':')[0], int( ep_url.split(':')[1] ) ) )
      s.shutdown(1)
      return True
   except:
      return False

def server_start_util(server, plc_ip ,myserv, myplc, MYSERV, MYPLC):
    danger = []
    info = []
    if isinstance(myserv,MYSERV):
        # Check if OPC Server is running
        if isOpen(server.endpoint_url):
            info.append[ "Server running at opc.tcp://"+server.endpoint_url ]
            try:
                # Connect to PLC 
                if plc_ip is not None:
                    myplc = MYPLC( serverid,plc_ip )
                else:
                    myplc = MYPLC( serverid )
                info.append(["PLC Connected"])
            except:
                danger.append["Couldn't connect top plc at: "+plc_ip ]

        else:
            danger.append([ "Server failed to start at opc.tcp://"+server.endpoint_url+". Check log file" ])
            
    else:
        try:
            myserv = MYSERV( server.id )   
            # server_start_util(server, plc_ip ,myserv, myplc, MYSERV, MYPLC)
        except:
            danger.append(["Couldn't launch server"])
    
    msgs = {
        'danger' : danger,
        'info' : info,
    }
    return myserv, myplc, msgs            
        