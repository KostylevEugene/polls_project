import bcrypt
from db import db_session
from models import User

name = 'admin'
email = "admin@mail.ru"
password = 'Odmen666'
role = "admin"

salt = bcrypt.gensalt()
hash_pass = bcrypt.hashpw(password.encode("utf8"), salt).decode("utf8")
admin = User(name, email, hash_pass, role)

db_session.add(admin)
db_session.commit()
