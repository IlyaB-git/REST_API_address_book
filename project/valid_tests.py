import re


def valid_client(name, surname, patronymic, gender, date_birthday, address):
    if len(name) < 3 or not name.isalpha():
        return False
    if len(surname) < 3 or not surname.isalpha():
        return False
    if len(patronymic) < 3 or not patronymic.isalpha():
        return False
    return True

def valid_phone(number):
    number = str(number)
    if len(number) == 12:
        if number[0:2] == '+7':
            number = '8' + number[2:]
    if len(number) == 11:
        if number[0] != '8':
            return False
        for i in number:
            if not i.isdigit():
                return False
        return True
    return False

def valid_email(email):
    pattern = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
    if re.match(pattern, email) is not None:
        return True
    else:
        return False
