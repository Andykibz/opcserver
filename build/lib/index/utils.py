import socket
types = {
    "int"
}

def custom_validation(form):
    status = True
    for k,v in form.items():
        if v is '':
            status = False
    return status

def Variable_Validation(form):
    status = True


def selectVals(objs):
    idlist = []
    namelist = []
    if objs:
        for obj in objs:
            idlist.append(obj.id)
            namelist.append(obj.object_name)
        return [('','Select Object')]+list(zip( idlist, namelist ))
    else:
        return [ ('', 'No Objects Defined' ) ]

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
