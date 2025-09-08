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
    text = CharField()
    author = ForeignKeyField(User)
    created_on = DateTimeField(default=datetime.now())

    @property
    def images(self):
        images = BlogImage.select().where(BlogImage.blog == self)
        return images

    @property
    def tags(self):
        tags = BlogTags.select().where(BlogTags.blog == self)
        return tags

    @property
    def comments(self):
        comments = Comment.select().where(Comment.blog == self)
        return comments


class BlogImage(Base):
    blog = ForeignKeyField(Blog)
    image_path = CharField(null=True)


class BlogTags(Base):
    blog = ForeignKeyField(Blog)
    text = CharField(null=True)


class Comment(Base):
    blog = ForeignKeyField(Blog)
    author = ForeignKeyField(User)
    text = CharField(null=True)
    created_on = DateTimeField(default=datetime.now())


db.connect()
db.create_tables((User, Blog, BlogImage, BlogTags, Comment))
