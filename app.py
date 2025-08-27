import hashlib

from flask import Flask

app = Flask(__name__)
app.config['SECRET_KEY'] = 'the random string'


def password_hash(password):
    hash_object = hashlib.sha256(password.encode()).hexdigest()
    return hash_object


def index():
    pass


def register():
    pass


def login():
    pass


def logout():
    pass


def create_post():
    pass
