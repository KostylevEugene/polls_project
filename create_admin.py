from db import db_session
from models import User

name = 'admin'
email = "admin@mail.ru"
password = 'Odmen666'
role = "admin"
admin = User(name, email, password, role)

db_session.add(admin)
db_session.commit()
