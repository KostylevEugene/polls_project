from db import db_session
from models import User, Poll

def signed_in_user(user_email):
    user = db_session.query(User.email).filter(User.email == user_email).scalar()
    return user

def get_password_by_email(email):
    password = db_session.query(User.password).filter(User.email == email).scalar()
    return password

def get_user_id(email):
    user_id = db_session.query(User.id).filter(User.email == email).scalar()
    return user_id

def get_poll_name(poll_name):
    name = db_session.query(Poll.polls_name).filter(Poll.polls_name == poll_name).scalar()
    return name


# if __name__ == "__main__":
# # #     print(type(signed_in_user('ef45@mail.eu')))
#     print(get_password_by_email('Jake@mail.eu'))