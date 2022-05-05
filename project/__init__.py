from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager
from flask_migrate import Migrate



app = Flask(__name__)
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'drgdgdfwhuirhsfow3uj39ojje'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user1:123@localhost/db_orion_test'
db = SQLAlchemy(app)
login_manager = LoginManager(app)


