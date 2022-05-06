from flask import jsonify
from flask_login import login_required, login_user, current_user
from project import app, request, db, login_manager
from project.models import User, Client, Phone, Email
from project.valid_tests import valid_client, valid_phone, valid_email
from project.logger import logger



@login_manager.user_loader
def load_user(user_id):
    return db.session.query(User).get(user_id)

@app.route('/login', methods=['POST',  'GET'])
@app.route('/login/', methods=['POST',  'GET'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter(username == username).first()
        if user and user.check_password(password):
            login_user(user)
            return jsonify('authorized')
        else:
            return jsonify('incorrect data')
    return jsonify('login page')


@app.route('/clients', methods=['POST', 'GET', 'PUT', 'DELETE', 'PATCH'])
@app.route('/clients/', methods=['POST', 'GET', 'PUT', 'DELETE', 'PATCH'])
@login_required
def client_view():
    logger.info(request.form)
    if request.method == 'PUT':
        try:
            name = request.form.get('name')
            surname = request.form.get('surname')
            patronymic = request.form.get('patronymic')
            gender = eval(request.form.get('gender'))
            date_birthday = request.form.get('date_birthday')
            address = request.form.get('address')
            if valid_client(name, surname, patronymic, gender, date_birthday, address):
                record = Client(name, surname, patronymic, gender, date_birthday, address)
                db.session.add(record)
                db.session.commit()
                logger.info('saved to db')
                return jsonify('Client saved')
            else:
                logger.info('valid failed')
                return jsonify('Valid test failed')
        except Exception as err:
            logger.error(err)
            return jsonify('Data base error')
    if request.method == 'POST':
        client_id = request.form.get('client_id')
        if client_id:
            try:
                client = Client.query.get(client_id)
                phones_set, emails_set = [], []
                for phone in Phone.query.filter(Phone.client_id == client_id).all():
                    phones_set.append({
                        'id': phone.id,
                        'type': phone.type,
                        'number': phone.number
                    })
                for email in Email.query.filter(Email.client_id == client_id).all():
                    emails_set.append({
                        'id': email.id,
                        'type': email.type,
                        'email': email.email
                    })
                res = {
                    'id': client.id,
                    'name': client.name,
                    'surname': client.surname,
                    'patronymic': client.patronymic,
                    'gender': client.gender,
                    'date_birthday': client.date_birthday,
                    'address': client.address,
                    'phones': phones_set,
                    'emails': emails_set
                }
                return jsonify(res)
            except Exception as err:
                logger.error(err)
                return jsonify('Data base error')
        else:
            try:
                res = []
                for client in Client.query:
                    phones_set, emails_set = [], []
                    for phone in Phone.query.filter(Phone.client_id == client.id).all():
                        phones_set.append({
                            'id': phone.id,
                            'type': phone.type,
                            'number': phone.number
                        })
                    for email in Email.query.filter(Email.client_id == client.id).all():
                        emails_set.append({
                            'id': email.id,
                            'type': email.type,
                            'email': email.email
                        })
                    res.append({
                        'id': client.id,
                        'name': client.name,
                        'surname': client.surname,
                        'patronymic': client.patronymic,
                        'gender': client.gender,
                        'date_birthday': client.date_birthday,
                        'address': client.address,
                        'phones': phones_set,
                        'emails': emails_set
                    })
                return jsonify(res)
            except Exception as err:
                logger.error(err)
                return jsonify('Data base error')

    if request.method == 'DELETE':
        client_id = request.form.get('client_id')
        if client_id:
            try:
                Client.query.filter(Client.id == client_id).delete()
                db.session.commit()
                logger.info('del to db')
                return jsonify('Client deleted')
            except Exception as err:
                logger.error(err)
                return jsonify('Data base error')
    if request.method == 'PATCH':
        client_id = request.form.get('client_id')
        if client_id:
            try:
                name = request.form.get('name')
                surname = request.form.get('surname')
                patronymic = request.form.get('patronymic')
                gender = bool(request.form.get('gender'))
                date_birthday = request.form.get('date_birthday')
                address = request.form.get('address')
                upd = dict()
                if name: upd['name'] = name
                if surname: upd['surname'] = surname
                if patronymic: upd['patronymic'] = patronymic
                if gender: upd['gender'] = gender
                if date_birthday: upd['date_birthday'] = date_birthday
                if address: upd['address'] = address
                if valid_client(name, surname, patronymic, gender, date_birthday, address):
                    Client.query.filter(Client.id==client_id).update(upd)
                    db.session.commit()
                    logger.info('updated to db')
                    return jsonify('Client updated')
                else:
                    logger.info('valid failed')
                    return jsonify('Valid test failed')
            except Exception as err:
                logger.error(err)
                return jsonify('Data base error')

    return jsonify('client page')


@app.route('/phones', methods=['POST', 'GET', 'PUT', 'DELETE', 'PATCH'])
@app.route('/phones/', methods=['POST', 'GET', 'PUT', 'DELETE', 'PATCH'])
@login_required
def phone_view():
    logger.info(request.form)
    if request.method == 'PUT':
        try:
            client_id = int(request.form.get('client_id'))
            type = eval(request.form.get('type'))
            number = request.form.get('number')
            if valid_phone(number):
                record = Phone(client_id, type, number)
                db.session.add(record)
                db.session.commit()
                logger.info('saved to db')
                return jsonify('Phone saved')
            else:
                logger.info('valid failed')
                return jsonify('Valid test failed')
        except Exception as err:
            logger.error(err)
            return jsonify('Data base error')
    if request.method == 'POST':
        phone_id = request.form.get('phone_id')
        client_id = request.form.get('client_id')
        if phone_id:
            try:
                phone = Phone.query.filter(Phone.id == phone_id).first()
                res = {
                    'id': phone.id,
                    'client_id': phone.client_id,
                    'type': phone.type,
                    'number': phone.number
                }
                return jsonify(res)
            except Exception as err:
                logger.error(err)
                return jsonify('Data base error')
        elif client_id:
            try:
                res = []
                phones = Phone.query.filter(Phone.client_id == client_id).all()
                for phone in phones:
                    res.append({
                        'id': phone.id,
                        'client_id': phone.client_id,
                        'type': phone.type,
                        'number': phone.number
                    })
                return jsonify(res)
            except Exception as err:
                logger.error(err)
                return jsonify('Data base error')
        else:
            try:
                res = []
                phones = Phone.query
                for phone in phones:
                    res.append({
                        'id': phone.id,
                        'client_id': phone.client_id,
                        'type': phone.type,
                        'number': phone.number
                    })
                return jsonify(res)
            except Exception as err:
                logger.error(err)
                return jsonify('Data base error')

    if request.method == 'DELETE':
        phone_id = request.form.get('phone_id')
        if phone_id:
            try:
                Phone.query.filter(Phone.id == phone_id).delete()
                db.session.commit()
                logger.info('del to db')
                return jsonify('Phone deleted')
            except Exception as err:
                logger.error(err)
                return jsonify('Data base error')
    if request.method == 'PATCH':
        phone_id = request.form.get('phone_id')
        if phone_id:
            try:
                client_id = request.form.get('client_id')
                type = request.form.get('type')
                number = request.form.get('number')
                upd = dict()
                if client_id: upd['client_id'] = client_id
                if type: upd['type'] = type
                if number: upd['number'] = number
                if valid_phone(number):
                    Phone.query.filter(Phone.id==phone_id).update(upd)
                    db.session.commit()
                    logger.info('updated to db')
                    return jsonify('Phone updated')
                else:
                    logger.info('valid failed')
                    return jsonify('Valid test failed')
            except Exception as err:
                logger.error(err)
                return jsonify('Data base error')

    return jsonify('Phone page')


@app.route('/emails', methods=['POST', 'GET', 'PUT', 'DELETE', 'PATCH'])
@app.route('/emails/', methods=['POST', 'GET', 'PUT', 'DELETE', 'PATCH'])
@login_required
def email_view():
    logger.info(request.form)
    if request.method == 'PUT':
        try:
            client_id = request.form.get('client_id')
            type = eval(request.form.get('type'))
            email = request.form.get('email')
            if valid_email(email):
                record = Email(client_id, type, email)
                db.session.add(record)
                db.session.commit()
                logger.info('saved to db')
                return jsonify('Email saved')
            else:
                logger.info('valid failed')
                return jsonify('Valid test failed')
        except Exception as err:
            logger.error(err)
            return jsonify('Data base error')
    if request.method == 'POST':
        email_id = request.form.get('email_id')
        client_id = request.form.get('client_id')
        if email_id:
            try:
                email = Email.query.get(email_id)
                res = {
                    'id': email.id,
                    'client_id': email.client_id,
                    'type': email.type,
                    'email': email.email
                }
                return jsonify(res)
            except Exception as err:
                logger.error(err)
                return jsonify('Data base error')
        elif client_id:
            try:
                res = []
                emails = Email.query.filter(Email.client_id == client_id).all()
                for email in emails:
                    res.append({
                        'id': email.id,
                        'client_id': email.client_id,
                        'type': email.type,
                        'email': email.email
                    })
                return jsonify(res)
            except Exception as err:
                logger.error(err)
                return jsonify('Data base error')
        else:
            try:
                res = []
                emails = Email.query
                for email in emails:
                    res.append({
                        'id': email.id,
                        'client_id': email.client_id,
                        'type': email.type,
                        'email': email.email
                    })
                return jsonify(res)
            except Exception as err:
                logger.error(err)
                return jsonify('Data base error')

    if request.method == 'DELETE':
        email_id = request.form.get('email_id')
        if email_id:
            try:
                Email.query.filter(Email.id == email_id).delete()
                db.session.commit()
                logger.info('del to db')
                return jsonify('Email deleted')
            except Exception as err:
                logger.error(err)
                return jsonify('Data base error')
    if request.method == 'PATCH':
        email_id = request.form.get('email_id')
        if email_id:
            try:
                client_id = request.form.get('client_id')
                type = request.form.get('type')
                email = request.form.get('email')
                upd = dict()
                if client_id: upd['client_id'] = client_id
                if type: upd['type'] = eval(type)
                if email: upd['email'] = email
                if valid_email(email):
                    Email.query.filter(Email.id==email_id).update(upd)
                    db.session.commit()
                    logger.info('updated to db')
                    return jsonify('Email updated')
                else:
                    logger.info('valid failed')
                    return jsonify('Valid test failed')
            except Exception as err:
                logger.error(err)
                return jsonify('Data base error')

    return jsonify('Email page')
