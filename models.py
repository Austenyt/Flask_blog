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

class
