from datetime import datetime
from index import db
import logging

class Server(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    server_name = db.Column( db.String(120), nullable=False )
    server_endpoint_url = db.Column( db.String(120), unique=True, nullable=False )
    server_namespace = db.Column( db.String(120), nullable=True, )
    server_created_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow )
    server_objects = db.relationship('Object',backref='server',cascade="all, delete-orphan" , lazy='dynamic')

    def __repr__( self ):
        return "Server: {}".format(self.server_name)

class Object(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    object_name = db.Column( db.String(120), nullable=False )
    object_parent_id = db.Column( db.Integer, nullable=True )
    object_server_id = db.Column(db.Integer,db.ForeignKey('server.id',ondelete='CASCADE'),nullable=False)
    object_variables = db.relationship("Variable", backref="object", cascade="all, delete-orphan" , lazy='dynamic' )

    def has_child( self ):    
        return True if Object.query.filter_by(object_parent_id=self.id) else False
    
    def is_parent( self ):
        return True if self.object_parent_id is None else False

    def get_parent( self ):        
        return Object.query.get( self.object_parent_id )

    def get_child_objects( self ):
        return self.query.filter_by(object_parent_id=self.id) if Object.query.filter_by(object_parent_id=self.id) else False

    def __repr__( self ):
        return "Object: {}".format(self.object_name)

class Variable( db.Model ):
    id = db.Column( db.Integer, primary_key=True )
    variable_name = db.Column( db.String(120), nullable=False )
    variable_type = db.Column( db.String(20), nullable=True )
    variable_writable = db.Column( db.Boolean(), nullable=False )
    variable_address = db.Column( db.String(120), nullable=False)
    variable_value = db.Column( db.String(100), nullable=True)
    variable_object_id = db.Column(db.Integer,db.ForeignKey('object.id',ondelete='CASCADE'),nullable=False )

    @staticmethod
    def validate( obj_id, address ):
        allvarrs =  Object.query.get(obj_id).object_variables.all()
        for var in allvarrs:
            if var.variable_address == address :
                return False
        return True                
                
    def __repr__( self ):
        return "Variable: {}".format(self.variable_name)
