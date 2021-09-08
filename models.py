from sqlalchemy import Column, Integer, String, ForeignKey

from db import Base, engine

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

class Poll(Base):
    __tablename__ = 'polls'

    id = Column(Integer(), primary_key=True)
    # ForeignKey проверяет наличие id в таблице User
    # index позволяет делать выборку по столбцу быстрее
    # nullable разрешает оставлять поле пустым
    user_id = Column(Integer(), ForeignKey(User.id), index=True, nullable=False)
    polls_name = Column(String(120))

    def __repr__(self):
        return f'Poll: {self.id}, {self.polls_name}'


class Questions(Base):
    __tablename__ = 'questions'

    id = Column(Integer(), primary_key=True)
    polls_id = Column(Integer(), ForeignKey(Poll.id), index=True, nullable=False)
    question = Column(String(240))

    def __repr__(self):
        return f'Question: {self.id}, {self.question}'


class Users_answers(Base):
    __tablename__ = 'users_answers'

    id = Column(Integer(), primary_key=True)
    user_id = Column(Integer(), ForeignKey(User.id), index=True, nullable=False)
    polls_id = Column(Integer(), ForeignKey(Poll.id), index=True, nullable=False)
    question_id = Column(Integer(), ForeignKey(Questions.id), index=True, nullable=False)
    answer = Column(String(60))

    def __repr__(self):
        return f'Answer: {self.id}, {self.answer}'


if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)

