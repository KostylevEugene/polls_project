from db import Base, engine
from marshmallow import Schema, fields
from sqlalchemy import Column, Integer, String, ForeignKey


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer(), primary_key=True)
    name = Column(String())
    email = Column(String(120), unique=True)
    password = Column(String())
    role = Column(String())

    def __init__(self, name, email, password, role):
        self.name = name
        self.email = email
        self.password = password
        self.role = role

    def __repr__(self):
        return f'User: {self.id}, {self.name}'


class UserSchema(Schema):
    id = fields.Int()
    name = fields.Str()
    email = fields.Email()
    password = fields.Str()
    role = fields.Str()


class Poll(Base):
    __tablename__ = 'polls'

    id = Column(Integer(), primary_key=True)
    # ForeignKey проверяет наличие id в таблице User
    # index позволяет делать выборку по столбцу быстрее (что это значит?)
    # nullable разрешает оставлять поле пустым
    user_id = Column(Integer(), ForeignKey(User.id), index=True, nullable=False)
    polls_name = Column(String(120))
    question = Column(String(1000))
    counter = Column(String(1000))
    access_level = Column(String(10))
    access_granted = Column(String(1000))

    def __init__(self, user_id, polls_name, question, counter, access_level, access_granted):
        self.user_id = user_id
        self.polls_name = polls_name
        self.question = question
        self.counter = counter
        self.access_level = access_level
        self.access_granted = access_granted

    def __repr__(self):
        return f'Poll: {self.id}, {self.polls_name}'


# class PollSchema(Schema):
#     polls_name = fields.Str()
#     questions = fields.Str()
#     access_level = fields.Str()
#     access_granted = fields.Str()


# class Questions(Base):
#     __tablename__ = 'questions'
#
#     id = Column(Integer(), primary_key=True)
#     polls_id = Column(Integer(), ForeignKey(Poll.id), index=True, nullable=False)
#     question = Column(String(1000))
#
#     def __init__(self, polls_id, question):
#         self.polls_id = polls_id
#         self.question = question
#
#     def __repr__(self):
#         return f'Question: {self.id}, {self.question}'


# class QuestionSchema(Schema):
#     id = fields.Int()
#     question = fields.Str()


class Users_answers(Base):
    __tablename__ = 'users_answers'

    id = Column(Integer(), primary_key=True)
    user_id = Column(Integer(), ForeignKey(User.id), index=True, nullable=False)
    polls_id = Column(Integer(), ForeignKey(Poll.id), index=True, nullable=False)
    answer = Column(String(1000))

    def __init__(self, user_id, polls_id, answer):
        self.user_id = user_id
        self.polls_id = polls_id
        self.answer = answer

    def __repr__(self):
        return f'Answer: {self.id}, {self.answer}'


# class Users_answersSchema(Schema):
#     id = fields.Int()
#     user_id = fields.Int()
#     polls_id = fields.Int()
#     question_id = fields.Int()
#     answer = fields.Str()


if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)

