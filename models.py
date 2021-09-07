from sqlalchemy import Column, Integer, String

from db import Base, engine

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer(), primary_key=True)
    name = Column(String())
    email = Column(String(120), unique=True)
    password = Column(String())
    role = Column(String())

    def __repr__(self):
        return f'User {self.id}, {self.name}'

class Poll(Base):
    __tablename__ = 'polls'

    id = Column(Integer(), primary_key=True)
    user_id = Column(Integer())
    polls_name = Column(String(120))

    def __repr__(self):
        return f'Poll {self.id}, {self.polls_name}'


class Questions(Base):
    __tablename__ = 'questions'

    id = Column(Integer(), primary_key=True)
    polls_id = Column(Integer())
    question = Column(String(240))
    answer = Column(String(120))


class Users_answers(Base):
    __tablename__ = 'users_answers'

    id = Column(Integer(), primary_key=True)
    user_id = Column(Integer())
    polls_id = Column(Integer())
    question_id = Column(Integer())
    answer = Column(String(60))


if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)

