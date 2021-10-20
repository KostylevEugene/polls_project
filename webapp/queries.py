from webapp.db import db_session
from webapp.models import User, Poll, Users_answers

def signed_in_user(user_email):
    user = db_session.query(User.email).filter(User.email == user_email).scalar()
    return user

def get_password_by_email(email):
    password = db_session.query(User.password).filter(User.email == email).scalar()
    return password

def get_user_id(email):
    user_id = db_session.query(User.id).filter(User.email == email).scalar()
    return user_id

def is_polls_name_exists(poll_name):
    subq = db_session.query(Poll).filter(Poll.polls_name == poll_name)
    return db_session.query(subq.exists()).scalar()

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
    return "Access granted" if user in access else 'Access denied'


def get_access_level_by_polls_id(polls_id):
    access = db_session.query(Poll.access_level).filter(Poll.id == polls_id).scalar()
    return access

def get_counter(polls_id):
    counter = db_session.query(Poll.counter).filter(Poll.id == polls_id).scalar()
    return counter

def is_answer_exists(user_id, polls_id):
    subq = db_session.query(Users_answers).filter(Users_answers.user_id == user_id and Users_answers.polls_id == polls_id)
    return db_session.query(subq.exists()).scalar()

def get_polls_name_by_id(polls_id):
    polls_name = db_session.query(Poll.polls_name).filter(Poll.id == polls_id).scalar()
    return polls_name

def get_access_level(polls_id):
    access_level = db_session.query(Poll.access_level).filter(Poll.id == polls_id).scalar()
    return access_level

def get_poll_for_changing(polls_id):
    poll = db_session.query(Poll.polls_name, Poll.question, Poll.access_level, Poll.access_granted).filter(Poll.id == polls_id).first()
    return poll

def get_answered_users(polls_id):
    users = db_session.query(Users_answers.user_id).filter(Users_answers.polls_id == polls_id).all()
    return users


# def update_counter(polls_id, counter):
#     db_session.query(Poll).filter(Poll.polls_id).update({'counter': counter}, synchronize_session='fetch')


# if __name__ == "__main__":
# # # #     print(type(signed_in_user('ef45@mail.eu')))
# # # #     print(get_password_by_email('Jake@mail.eu'))
# # # #     print(get_polls_list('icds@mail.eu'))
# # # #     print(get_polls_id('Computer73'))
# # # #     print(get_email_in_access_granted())
# # # #     print(get_access_level_by_polls_id(1))
# # #     # print(get_email_from_access_granted('o@mail.us', 5))
# # #     # print(get_questions_by_poll_id(5))
# # #     # print(get_counter(7))
# # #     print(get_answer(2, 8))
#     print(get_poll_for_changing(10))
#     print(len(get_answered_users(8)))