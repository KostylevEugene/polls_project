from db import db_session
from models import User

def signed_in_user(user_email):
    user = db_session.query(User.email).filter(User.email == user_email).scalar()
    return user

# if __name__ == "__main__":
#     print(type(signed_in_user('ef45@mail.eu')))