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

def get_polls_list(email):
    id = db_session.query(User.id).filter(User.email == email).scalar()
    raw_polls_list = db_session.query(Poll.polls_name).filter(Poll.user_id == id).all()

    poll_list = []

    for i in raw_polls_list:
        for j in i:
            poll_list.append(j)

    return poll_list

def get_polls_id(poll_name):
    polls_id = db_session.query(Poll.id).filter(Poll.polls_name == poll_name).scalar()
    return polls_id

def get_questions_by_poll_id(poll_id):
    questions = db_session.query(Poll.question).filter(Poll.id == poll_id).scalar()
    return questions

def get_email_from_access_granted(user, polls_id):
    access = db_session.query(Poll.access_granted).filter(Poll.id == polls_id).scalar()
    return True if user in access else False


def get_access_level_by_polls_id(polls_id):
    access = db_session.query(Poll.access_level).filter(Poll.id == polls_id).scalar()
    return access


# if __name__ == "__main__":
#     print(type(signed_in_user('ef45@mail.eu')))
#     print(get_password_by_email('Jake@mail.eu'))
#     print(get_polls_list('icds@mail.eu'))
#     print(get_polls_id('Computer73'))
#     print(get_email_in_access_granted())
#     print(get_access_level_by_polls_id(1))
#     print(get_email_from_access_granted('o@mail.us', 5))