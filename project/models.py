from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from project import db


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password_hash = db.Column(db.String(102), nullable=False)
    created_on = db.Column(db.DateTime(), default=datetime.utcnow)
    updated_on = db.Column(db.DateTime(), default=datetime.utcnow,  onupdate=datetime.utcnow)

    def __init__(self, username, password):
        self.username = username
        self.set_password(password)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Client(db.Model):
    __tablename__ = 'clients'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    surname = db.Column(db.String(64), nullable=False)
    patronymic = db.Column(db.String(64), nullable=False)
    gender = db.Column(db.Boolean(), nullable=False)    #True for male; False for female
    date_birthday = db.Column(db.Date, nullable=False)
    address = db.Column(db.Text, nullable=False)
    phones = db.relationship('Phone', backref=db.backref('phone_user', lazy=True))
    emails = db.relationship('Email', backref=db.backref('email_user', lazy=True))

    def __init__(self, name, surname, patronymic, gender, date_birthday, address):
        self.name = name
        self.surname = surname
        self.patronymic = patronymic
        self.gender = gender
        self.date_birthday = date_birthday
        self.address = address


class Phone(db.Model):
    __tablename__ = 'phones'
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'))
    type = db.Column(db.Boolean, nullable=False)    #True is mobile; False is city
    number = db.Column(db.String(16), nullable=False, unique=True)

    def __init__(self, client_id, type, number):
        self.client_id = client_id
        self.type = type
        self.number = number

class Email(db.Model):
    __tablename__ = 'emails'
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'))
    type = db.Column(db.Boolean, nullable=False)  # True is personal; False is worker
    email = db.Column(db.String(256), nullable=False, unique=True)

    def __init__(self, client_id, type, email):
        self.client_id = client_id
        self.type = type
        self.email = email

# db.create_all()
