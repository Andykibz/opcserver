from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SECRET_KEY'] = 'f1d9d48ec0e26e2a250839fa36ea2c602cc4f85ccfeb5c65'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
from flask_wtf.csrf import CSRFProtect
csrf = CSRFProtect(app)
db = SQLAlchemy(app)

from index import routes
