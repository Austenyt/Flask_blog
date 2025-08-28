import hashlib

from flask import *

from models import User

app = Flask(__name__)
app.config['SECRET_KEY'] = 'the random string'


def password_hash(password):
    hash_object = hashlib.sha256(password.encode()).hexdigest()
    return hash_object


def index():
    pass


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        password = request.form['password']
        password_confirm = request.form['password_confirm']
        image = request.files.get('image')
        if password != password_confirm:
            return render_template('register.html', error='Пароли не совпадают')
        try:
            User.create(
                first_name=first_name,
                last_name=last_name,
                email=email,
                password_hash=password_hash(password),
                image_path=image,
            )
            return redirect(url_for('index'))
        except Exception as error:
            return render_template('register.html', error=error)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        email = request.form['email']
        password = request.form['password']
        user = User.get_or_none(User.email == email)

        if user:
            if user.password_hash == password_hash(password):
                session['user_id'] = user.id
                session['email'] = user.email
                return redirect(url_for('index'))
            else:
                return render_template('login.html', error='Неверный пароль')
        else:
            return render_template('login.html', error='Пользователь не найден')


def logout():
    pass


def create_post():
    pass
