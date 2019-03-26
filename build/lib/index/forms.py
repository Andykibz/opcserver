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
                                            'placeholder': "Namespace"
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

    var_type = HiddenField('Data Type',default='NoneType')

    writable = BooleanField('Writable',id="check_writable", render_kw = {
                                            'placeholder': "Writable"
                                        }
                                )
    address = StringField('Address', validators=[ DataRequired() ],
                            render_kw = { 'placeholder': "Address"
                                }
                            )

    var_object = SelectField('Object',validators=[ DataRequired() ] )

    value = StringField('Default Value',            
                                render_kw = {
                                            'placeholder': "Value"
                                        }
                                )

    submit = SubmitField('Add Variable')
