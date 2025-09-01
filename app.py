import hashlib
import os

from flask import *

from models import User, Blog

app = Flask(__name__)
app.config['SECRET_KEY'] = 'the random string'


def password_hash(password):
    hash_object = hashlib.sha256(password.encode()).hexdigest()
    return hash_object


@app.before_request
def get_user():
    user_id = session.get('user_id')
    if user_id:
        user = User.get_or_none(User.id == user_id)
    else:
        user = None
    request.user = user


@app.route('/')
def index():
    posts = Blog.select().join(User).order_by(Blog.id.desc())
    return render_template('blog.html', posts=posts, user=request.user)


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


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    del session['user_id']
    return redirect(url_for('index'))


@app.route('/add_post', methods=['GET', 'POST'])
def add_post():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        name = request.form['name']
        text = request.form['text']
        author = session['user_id']
        image = request.files.get('image')
        if image:
            image.save('media/' + image.filename)
            image = 'media/' + image.filename
        else:
            image = None

        Blog.create(
            name=name,
            text=text,
            author=author,
            image_path=image,
        )
        return redirect(url_for('index'))
    return render_template('add_post.html')


@app.route('/edit_post/<int:post_id>', methods=['GET', 'POST'])
def edit_post(post_id):
    post = Blog.get(Blog.id == post_id)
    if post.author != request.user:
        return redirect(url_for('index'))
    else:
        if request.method == 'GET':
            return render_template('edit_post.html')
        else:
            name = request.form['name']
            text = request.form['text']
            image = request.files.get('image')
            if image:
                image.save('media/' + image.filename)
                image = 'media/' + image.filename
            else:
                image = None
        post.name = name
        post.text = text
        post.save()
        return redirect(url_for('post_detail', post_id=post_id))


@app.route('/post/<int:post_id>', methods=['GET'])
def post_detail(post_id):
    post = Blog.get(Blog.id == post_id)
    return render_template('post_detail.html', post=post)


@app.route('/media/<filename>')
def media(filename):
    return send_from_directory(directory=os.path.dirname('media/' + filename),
                               path=os.path.basename('media/' + filename))


@app.route('/profile', methods=['GET'])
def profile():
    if session.get('user_id'):
        user = User.get_or_none(User.id == session['user_id'])
    else:
        user = None

    return render_template('profile.html', user=user)


if __name__ == '__main__':
    app.run(debug=True)
