
def valid_user(name, surname, patronymic, gender, date_birthday, address):
    if len(name) < 3 or not name.isalpha():
        return False
    if len(surname) < 3 or not surname.isalpha():
        return False
    if len(patronymic) < 3 or not patronymic.isalpha():
        return False
    return True

def valid_phone(number):
    return True

def valid_email(email):
    return True
