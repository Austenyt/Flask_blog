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
from datetime import datetime

from peewee import *

db = SqliteDatabase('blog.db')


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
    name = CharField()
    image_path = CharField(null=True)
    text = CharField()
    author = ForeignKeyField(User)
    created_on = DateTimeField(default=datetime.now())


db.connect()
db.create_tables((User, Blog))
