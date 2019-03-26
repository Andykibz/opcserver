from flask import (render_template, flash, url_for, jsonify,request,redirect)
from index import app,db
from index.models import Server,Object, Variable
from index.forms import ServerCreateForm,ObjectCreateForm,VariableCreateForm
from . import utils
from myserver import MyServer
from myplc import MyPlc
from snap7.snap7exceptions import Snap7Exception
import time

class Control(MyServer,MyPlc):
    def __init__(self):
        self.ip = None        

    def get_db(self, server_id,ip=None):
        self.db_server = Server.query.get(server_id)
        if ip is not None:
            self.ip = ip
        self.inits()
    
    def inits(self):
        MyServer.__init__(self)
        MyPlc.__init__(self)
    
    def set_opc(self):
        self.instantiate_server_vars()

    def make_tags_dict(self,allvars):
        for var in allvars:
            self.varsdict[var.variable_address] = {
                'obj'   : self.opc_variables_dict[var.variable_address],
                'type'  : var.variable_type
            }

# global ms,mp
global ctrl
ctrl = Control()

@app.route("/")
def home():
    servers = Server.query.all()
    form = ServerCreateForm()
    return render_template('index.html',form=form,servers=servers)

@app.route("/",methods= ['POST','GET'] )
def create_server():
    form = ServerCreateForm()
    if form.validate_on_submit():
        server = Server( server_name=form.server_name.data, 
        server_endpoint_url=form.endpoint_url.data,server_namespace=form.namespace.data )
        db.session.add(server)
        db.session.commit()
        resp = {
            'message' : '{} Created Successfully'.format(form.server_name.data),
            'servers' : Server.query.all()
        }
        return redirect(url_for('home'))
    return jsonify(data=form.errors)

@app.route("/server/<serverid>/edit",methods= ['POST'] )    
def edit_server( serverid ):
    form = ServerCreateForm()
    if form.validate_on_submit():
        server = Server.query.get( serverid )
        server.server_name = form.server_name.data
        server.server_endpoint_url = form.endpoint_url.data
        server.server_namespace = form.namespace.data
        db.session.add( server )
        db.session.commit()
        flash('{} Edited Successfully'.format(server.server_name), 'success')
        return redirect(url_for('home'))
    flash('Could not edit Server' 'danger')
    return redirect(url_for('home'))            

@app.route("/server/delete/<serverid>",methods= ['POST'] )    
def delete_server( serverid ):
    server = Server.query.get( serverid )
    servername = server.name
    db.session.delete(server)
    db.session.commit()
    flash('{} Deleted Successfully'.format(servername), 'success')
    return redirect(url_for('create_server'))


@app.route("/server/<serverid>",methods= ['GET'] )
def server_populate(serverid):
    server = Server.query.get( serverid )
    objform = ObjectCreateForm()
    varform = VariableCreateForm()
    objects = server.server_objects
    varform.var_object.choices = utils.selectVals(objects)
    # objform.parent_object.choices = selectVals(objects)
    # vars = server.server_objects
    return render_template('server.html',
             objects=objects,
             server=server, 
             objform = ObjectCreateForm(),
             varform=varform
    )
@app.route("/start_server/<serverid>",methods=['POST'])
def start_server(serverid):
    if request.method=='POST' and request.form: 
        server = Server.query.get(request.form['server'])
        ctrl.get_db(server.id)
        try:
            ctrl.opc_server.start()
        except OSError as ipexp:
            return jsonify({ 'warning':'The endpoint: {} is currently being used'.format(server.server_endpoint_url) })
        else:     
            ctrl.connections()            
            return jsonify({ 'success':'PLC Connected' })

        return jsonify({ 'success':'Server running at {}'.format( server.server_endpoint_url ) })

    else:
        return jsonify("Web Server Error")


@app.route("/stop_server/<serverid>",methods=['GET'])
def stop_server(serverid):
    server = Server.query.get( serverid )
    ctrl.kill_threads()
    ctrl.opc_server.stop()
    return jsonify({"info":"Server at {} Stopped".format(server.server_endpoint_url)})
    


@app.route("/create_object",methods= ['POST'] )
def create_object():
    objform = ObjectCreateForm()
    
    serverobj = Server.query.get(objform.server.data)
    if request.method=='POST' and request.form:        
        obj = Object(   object_name = request.form['object_name'],
                        object_parent_id = request.form['parent_object'] if request.form['parent_object'] else None,
                        server = Server.query.get(request.form['server']) 
                    )
        db.session.add(obj)
        db.session.commit()
        return redirect( url_for('server_populate',serverid=serverobj.id) )
    else:    
        flash('Could not create {} object'.format(objform.object_name))
        return redirect(url_for('server_populate',serverid=serverobj.id))


@app.route("/create_variable,<server_id>/",methods= ['POST'] )
def create_variable(server_id):
    varform = VariableCreateForm()
    # obj = Object.query.get(varform.var_object.data)
    if utils.custom_validation( varform.data ):                
        if Variable.validate(varform.var_object.data,varform.address.data):
            try:
                var = Variable( variable_name=varform.name.data, variable_type=varform.var_type.data,
                        variable_writable=varform.writable.data, variable_address=varform.address.data,
                        variable_value=varform.value.data, object=Object.query.get(varform.var_object.data),
                         )
            except AttributeError as aexp:
                flash('Ensure all fields are filled','warning')                         
                return redirect( url_for('server_populate',serverid=server_id) )                             
        else:
            flash('The address {} has already been taken'.format(varform.address.data),'warning')                         
            return redirect( url_for('server_populate',serverid=server_id) )                         

        
        try:
            db.session.add(var)
            db.session.commit() 
        except AttributeError as aexp:
            flash('Ensure all fields are filled','warning')                         
            return redirect( url_for('server_populate',serverid=server_id) )                   
        except Exception as exp:
            flash('Could not save Variable'.format(varform.name.data))                
        else:
            flash('{} Created Successfully'.format(var.variable_name),'success')
            return redirect(url_for('server_populate',serverid=server_id))
            
    else:    
        flash( 'Could not create {} Variable'.format(varform.name.data), 'danger' )
        return redirect(url_for('server_populate',serverid=server_id))


@app.route("/variables/<var_id>/delete",methods= ['GET'] )
def delete_var(var_id):
    var = Variable.query.get(var_id)
    db.session.delete(var)
    db.session.commit()
    return jsonify("Deleted Successfully")

@app.route("/delete_object",methods= ['POST'] )
def delete_object():
    obj = Object.query.get(request.form['object_id'])
    objName = obj.name
    server_id = request.form['server_id']

    db.session.delete( obj )
    db.session.commit()
    flash('{} Deleted SUccessfully'.format(objName), 'success')
    return redirect(url_for('server_populate',serverid=server_id))
    