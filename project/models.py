from project import db




class User(db.Model):
    __tablename__ = 'users'
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
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    type = db.Column(db.Boolean, nullable=False)    #True is mobile; False is city
    number = db.Column(db.String(16), nullable=False, unique=True)

    def __init__(self, user_id, type, number):
        self.user_id = user_id
        self.type = type
        self.number = number

class Email(db.Model):
    __tablename__ = 'emails'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    type = db.Column(db.Boolean, nullable=False)  # True is personal; False is worker
    email = db.Column(db.String(256), nullable=False, unique=True)

    def __init__(self, user_id, type, email):
        self.user_id = user_id
        self.type = type
        self.email = email

# db.create_all()
