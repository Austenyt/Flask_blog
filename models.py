"""
Пользователь:
Имя
Фамилия
емаил (регистрация)
пароль
аватарка

Пост:
название
картинка (необязательно)
текст
автор
дата создания (автоматически)

"""
from peewee import *

db = SqliteDatabase('cats.db')


class Base(Model):
    class Meta:
        database = db


class User(Base):
    first_name = CharField()
    last_name = CharField()
    email = CharField(unique=True)
    password_hash = CharField()
    image_path = CharField(null=True)


class Blog(Base):



db.connect()
db.create_tables(User)
