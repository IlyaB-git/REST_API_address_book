from flask import jsonify
from project import app, request, db
from models import User, Phone, Email
from project.valid_test import valid_user, valid_phone, valid_email
from project.logger import logger


@app.route('/user', methods=['POST', 'GET', 'PUT', 'DELETE', 'PATCH'])
@app.route('/user/', methods=['POST', 'GET', 'PUT', 'DELETE', 'PATCH'])
def user_view():
    logger.info(request.form)
    if request.method == 'PUT':
        try:
            name = request.form.get('name')
            surname = request.form.get('surname')
            patronymic = request.form.get('patronymic')
            gender = eval(request.form.get('gender'))
            date_birthday = request.form.get('date_birthday')
            address = request.form.get('address')
            if valid_user(name, surname, patronymic, gender, date_birthday, address):
                record = User(name, surname, patronymic, gender, date_birthday, address)
                db.session.add(record)
                db.session.commit()
                return jsonify('User saved')
            else:
                return jsonify('Valid test failed')
        except Exception as err:
            logger.error(err)
            return jsonify('Data base error')
    if request.method == 'POST':
        user_id = request.form.get('user_id')
        if user_id:
            try:
                user = User.query.get(user_id)
                phones_set, emails_set = [], []
                for phone in Phone.query.filter(Phone.user_id == user_id).all():
                    phones_set.append({
                        'id': phone.id,
                        'type': phone.type,
                        'number': phone.number
                    })
                for email in Email.query.filter(Email.user_id == user_id).all():
                    emails_set.append({
                        'id': email.id,
                        'type': email.type,
                        'email': email.email
                    })
                res = {
                    'id': user.id,
                    'name': user.name,
                    'surname': user.surname,
                    'patronymic': user.patronymic,
                    'gender': user.gender,
                    'date_birthday': user.date_birthday,
                    'address': user.address,
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
                for user in User.query:
                    phones_set, emails_set = [], []
                    for phone in Phone.query.filter(Phone.user_id == user.id).all():
                        phones_set.append({
                            'id': phone.id,
                            'type': phone.type,
                            'number': phone.number
                        })
                    for email in Email.query.filter(Email.user_id == user.id).all():
                        emails_set.append({
                            'id': email.id,
                            'type': email.type,
                            'email': email.email
                        })
                    res.append({
                        'id': user.id,
                        'name': user.name,
                        'surname': user.surname,
                        'patronymic': user.patronymic,
                        'gender': user.gender,
                        'date_birthday': user.date_birthday,
                        'address': user.address,
                        'phones': phones_set,
                        'emails': emails_set
                    })
                return jsonify(res)
            except Exception as err:
                logger.error(err)
                return jsonify('Data base error')

    if request.method == 'DELETE':
        user_id = request.form.get('user_id')
        if user_id:
            try:
                User.query.filter(User.id == user_id).delete()
                db.session.commit()
                return jsonify('User deleted')
            except Exception as err:
                logger.error(err)
                return jsonify('Data base error')
    if request.method == 'PATCH':
        user_id = request.form.get('user_id')
        if user_id:
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
                User.query.filter(User.id==user_id).update(upd)
                db.session.commit()
                return jsonify('Updated')
            except Exception as err:
                logger.error(err)
                return jsonify('Data base error')

    return jsonify('User page')


@app.route('/phone', methods=['POST', 'GET', 'PUT', 'DELETE', 'PATCH'])
@app.route('/phone/', methods=['POST', 'GET', 'PUT', 'DELETE', 'PATCH'])
def phone_view():
    logger.info(request.form)
    if request.method == 'PUT':
        try:
            user_id = int(request.form.get('user_id'))
            type = eval(request.form.get('type'))
            number = request.form.get('number')
            if valid_phone(number):
                record = Phone(user_id, type, number)
                db.session.add(record)
                db.session.commit()
                return jsonify('Phone saved')
            else:
                return jsonify('Valid test failed')
        except Exception as err:
            logger.error(err)
            return jsonify('Data base error')
    if request.method == 'POST':
        phone_id = request.form.get('phone_id')
        user_id = request.form.get('user_id')
        if phone_id:
            try:
                phone = Phone.query.filter(Phone.id == id).first()
                res = {
                    'id': phone.id,
                    'user_id': phone.user_id,
                    'type': phone.type,
                    'number': phone.number
                }
                return jsonify(res)
            except Exception as err:
                logger.error(err)
                return jsonify('Data base error')
        elif user_id:
            try:
                res = []
                phones = Phone.query.filter(Phone.user_id == user_id).all()
                for phone in phones:
                    res.append({
                        'id': phone.id,
                        'user_id': phone.user_id,
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
                        'user_id': phone.user_id,
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
                return jsonify('Phone deleted')
            except Exception as err:
                logger.error(err)
                return jsonify('Data base error')
    if request.method == 'PATCH':
        id = request.form.get('phone_id')
        if id:
            try:
                user_id = request.form.get('user_id')
                type = request.form.get('type')
                number = request.form.get('number')
                upd = dict()
                if user_id: upd['user_id'] = user_id
                if type: upd['type'] = type
                if number: upd['number'] = number
                Phone.query.filter(Phone.id==id).update(upd)
                db.session.commit()
                return jsonify('Phone updated')
            except Exception as err:
                logger.error(err)
                return jsonify('Data base error')

    return jsonify('Phone page')


@app.route('/email', methods=['POST', 'GET', 'PUT', 'DELETE', 'PATCH'])
@app.route('/email/', methods=['POST', 'GET', 'PUT', 'DELETE', 'PATCH'])
def email_view():
    logger.info(request.form)
    if request.method == 'PUT':
        try:
            user_id = request.form.get('user_id')
            type = eval(request.form.get('type'))
            email = request.form.get('email')
            if valid_email(email):
                record = Email(user_id, type, email)
                db.session.add(record)
                db.session.commit()
                return jsonify('Email saved')
            else:
                return jsonify('Valid test failed')
        except Exception as err:
            logger.error(err)
            return jsonify('Data base error')
    if request.method == 'POST':
        email_id = request.form.get('email_id')
        user_id = request.form.get('user_id')
        if email_id:
            try:
                email = Email.query.get(email_id)
                res = {
                    'id': email.id,
                    'user_id': email.user_id,
                    'type': email.type,
                    'email': email.email
                }
                return jsonify(res)
            except Exception as err:
                logger.error(err)
                return jsonify('Data base error')
        elif user_id:
            try:
                res = []
                emails = Email.query.filter(Email.user_id == user_id).all()
                for email in emails:
                    res.append({
                        'id': email.id,
                        'user_id': email.user_id,
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
                for user in User.query:
                    res.append({
                        'id': user.id,
                        'name': user.name,
                        'surname': user.surname,
                        'patronymic': user.patronymic,
                        'gender': user.gender,
                        'date_birthday': user.date_birthday,
                        'address': user.address,
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
                return jsonify('Email deleted')
            except Exception as err:
                logger.error(err)
                return jsonify('Data base error')
    if request.method == 'PATCH':
        email_id = request.form.get('email_id')
        if email_id:
            try:
                user_id = request.form.get('user_id')
                type = request.form.get('type')
                email = request.form.get('email')
                upd = dict()
                if user_id: upd['user_id'] = user_id
                if type: upd['type'] = type
                if email: upd['number'] = email
                Email.query.filter(Email.id==id).update(upd)
                db.session.commit()
                return jsonify('Email updated')
            except Exception as err:
                logger.error(err)
                return jsonify('Data base error')

    return jsonify('Email page')
