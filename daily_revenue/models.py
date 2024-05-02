from app import db, app, manager
from flask_login import UserMixin
from datetime import datetime


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    password = db.Column(db.String(30), nullable=False)

class Price(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name_service = db.Column(db.String(30), unique=True, nullable=False)
    car = db.Column(db.Integer(), nullable=False)
    jeep = db.Column(db.Integer(), nullable=False)
    minivan = db.Column(db.Integer(), nullable=False)

class Employees(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    post = db.Column(db.String(30), nullable=False)

class Calculate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name_service = db.Column(db.String(30), nullable=False)
    percent = db.Column(db.Integer(), nullable=False)
    
class Report(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, default=datetime.now().date())
    username = db.Column(db.String(30), nullable=False)
    name_service = db.Column(db.String(30), nullable=False)
    amount = db.Column(db.Integer(), nullable=False)
    salary = db.Column(db.Integer(), nullable=False)

@manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

with app.app_context():
    db.create_all()