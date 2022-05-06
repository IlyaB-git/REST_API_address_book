from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate



app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'drgdgdfwhuirhsfow3uj39ojje'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user1:123@localhost/db_address_book'
db = SQLAlchemy(app)
login_manager = LoginManager(app)


