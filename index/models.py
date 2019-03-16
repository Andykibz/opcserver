from datetime import datetime
from index import db

class Server(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column( db.String(120), nullable=False )
    endpoint_url = db.Column( db.String(120), unique=True, nullable=False )
    namespace = db.Column( db.String(120), nullable=True, )
    created_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow )
    objects = db.relationship('Object',backref='server')

    def __repr__( self ):
        return f"Server: '{self.name}'"

class Object(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column( db.String(120), nullable=False )
    parent_id = db.Column( db.Integer, nullable=True )
    server_id = db.Column(db.Integer,db.ForeignKey('server.id',ondelete='CASCADE'),nullable=False)
    variables = db.relationship("Variable", backref="object")

    def has_child( self ):    
        return True if Object.query.filter_by(parent_id=self.id) else False
    
    def is_parent( self ):
        return True if self.parent_id is None else False

    def get_child_objects( self ):
        return self.query.filter_by(parent_id=self.id) if Object.query.filter_by(parent_id=self.id) else False

    def __repr__( self ):
        return f"Object: '{self.name}'"

class Variable(db.Model):
    id = db.Column( db.Integer, primary_key=True )
    name = db.Column( db.String(120), nullable=False )
    type = db.Column( db.String(20), nullable=False )
    writable = db.Column( db.Boolean(), nullable=False )
    tag_id = db.Column( db.String(120), nullable=False, unique=True)
    value = db.Column( db.String(100), nullable=False)
    object_id = db.Column(db.Integer,db.ForeignKey('object.id',ondelete='CASCADE'),nullable=False )

    def __repr__( self ):
        return f"Variable: '{ self.name }'"
