from flask_wtf import FlaskForm,Form
from wtforms import StringField,SubmitField,SelectField,HiddenField,BooleanField
from wtforms.validators import DataRequired
from index.models import Server,Object


class ServerCreateForm( FlaskForm ):

    server_name = StringField('Server',
                                validators=[ DataRequired() ],
                                render_kw = { 'placeholder': "Server Name"
                                        }
                                )

    endpoint_url = StringField('Endpoint Url',
                                validators=[ DataRequired() ],
                                render_kw = {
                                            'placeholder': "Endpoint URL"
                                        }
                                )

    namespace = StringField('Namespace',
                                render_kw = {
                                            'placeholder': "Project Name"
                                        }
                                )

    submit = SubmitField('Create Server',id="create_server_button")

class ObjectCreateForm( FlaskForm ):

    object_name = StringField('Object Name',
                                validators=[ DataRequired() ],
                                render_kw = {
                                            'placeholder': "Object Name"
                                        }
                                )

    server = HiddenField('Server',
                                validators=[ DataRequired() ],
                                render_kw = {
                                            'placeholder': 'Server'
                                        }
                                )                                

    submit = SubmitField('Add Object')


class VariableCreateForm( FlaskForm ):

    name = StringField('Variable Name',
                                validators=[ DataRequired() ],
                                render_kw = {
                                            'placeholder': "Variable Name"
                                        }
                                )

    var_type = SelectField('Data Type',
                                validators=[ DataRequired() ],
                                choices=[ ( '','Select Type' ), ( 'int', 'Integer' ),( 'bool', 'Boolean' ),('float','Floating Point'),('string','String') ],
                                render_kw = {
                                            'placeholder': "Project Name"
                                        }
                                )

    writable = BooleanField('Writable',id="check_writable", render_kw = {
                                            'placeholder': "Writable"
                                        }
                                )
    tag = StringField('Tag', validators=[ DataRequired() ],
                            render_kw = { 'placeholder': "Tag ID"
                                }
                            )

    var_object = SelectField('Object',validators=[ DataRequired() ] )

    value = StringField('Default Value',
                                validators=[ DataRequired() ],
                                render_kw = {
                                            'placeholder': "Value"
                                        }
                                )

    submit = SubmitField('Add Variable')
