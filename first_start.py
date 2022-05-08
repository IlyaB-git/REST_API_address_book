from time import sleep
from threading import Thread
from my_requests import login, make_random_clients
from project.models import db, User
from runner import app

def run():
    app.run()

def add_admin_and_clients():
    db.create_all()

    admin = User('admin', 'admin')
    db.session.add(admin)
    db.session.commit()

    login()
    make_random_clients()
    print('Done!')

Thread(target=run).start()
sleep(2)
Thread(target=add_admin_and_clients()).start()
