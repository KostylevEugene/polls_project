from config import DB_ENGINE
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base     # (?) для определения (или помощи создания) таблиц и моделей
from sqlalchemy.orm import sessionmaker, scoped_session

engine = create_engine(DB_ENGINE)                                         # показываем к какой базе будем подключаться
db_session = scoped_session(sessionmaker(bind=engine))          # позволяет коммуницировать с БД

Base = declarative_base()                           # все следующие модели будут наследоваться от этой переменной
Base.query = db_session.query_property()            # возможность делать запросы используя модели
