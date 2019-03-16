
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
            namelist.append(obj.name)
        return [(None,'Object')]+list(zip( idlist, namelist ))
    else:
        return [ (None, 'No Objects Defined' ) ]

def convert_val(val,vtype):
    if vtype is 'int':
        return int(val)
    elif vtype is 'float':        
        return float(val)
    elif vtype is 'string':        
        return str(val)
    elif vtype is 'bool':        
        if val is True or val is true or val is 1:
            return True
        else:
            return False
    else:
        return val            



