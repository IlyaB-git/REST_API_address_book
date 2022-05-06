### REST API сервер «Адресная книга»
Для запуска: указать в ```__init__.py``` в переменную ```app.config['SQLALCHEMY_DATABASE_URI']```
адрес к базе данных и запустить ```first_start.py``` (он также создаст 100 случайных записей)
предварительно поменяв имя и пароль.

Все функции для обращения к серверу можно взять из ```my_requests.py```   

```http://127.0.0.1:5000/login/``` - авторизация через POST (username, password)  
```http://127.0.0.1:5000/clients/``` - доступ к таблице пользователей  
```http://127.0.0.1:5000/phones/``` - доступ к таблице телефонов  
```http://127.0.0.1:5000/emails/``` - доступ к таблице эл. почт  

### Атрибуты сущностей:  
#### Пользователь:  
- имя - name  
- фамилия - surname  
- отчество - patronymic  
- пол - gender (True - муж, False - жен)  
- дата рождения - date_birthday  
- адрес - address  
- телефоны - phones  
- эл. адреса - emails  


#### Телефоны:  
- ID пользователя - client_id  
- Вид - type (True - Мобильный/False - Городской)  
- Номер телефона - number  

#### Электронные адреса:  
- ID пользователя - client_id  
- Вид - type (True - Личная/False - Рабочая)  
- Email - email  

### CRUD
Каждая сущность имеет методы ```['POST', 'PUT', 'DELETE', 'PATCH']```

#### Пользователь:
PUT:  name, surname, patronymic, gender, date_birthday, address  
POST: без параметров - получение всех записей, с параметром client_id - получение одной записи  
PATCH: client_id и необходимые параметры  
DELETE: только client_id

#### Телефон:  
PUT: client_id, type, number  
POST: без параметров - получение всех записей, с параметром phone_id получение записи, с параметром client_id - получение записей пользователя  
PATCH: phone_id и необходимые параметры  
DELETE: только phone_id

#### Email:  
PUT: client_id, type, email  
POST: без параметров - получение всех записей, с параметром email_id получение записи, с параметром client_id - получение записей пользователя  
PATCH: email_id и необходимые параметры  
DELETE: только email_id