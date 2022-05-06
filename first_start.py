from my_requests import login, make_random_clients
from project.models import db, User


db.create_all()

admin = User('admin', 'admin')
db.session.add(admin)
db.session.commit()

login()
make_random_clients()
