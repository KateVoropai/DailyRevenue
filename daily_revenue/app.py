from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import uuid
from flask_login import LoginManager
from flask_toastr import Toastr


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///daily_revenue.db'
app.config['SECRET_KEY'] = str(uuid.uuid4())
manager = LoginManager(app)

db = SQLAlchemy(app)
toastr = Toastr(app)