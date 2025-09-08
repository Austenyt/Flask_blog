import hashlib
import os

from flask import *
from werkzeug.utils import secure_filename

from models import User, Blog, BlogImage, BlogTags, Comment

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


def render(template, **kwargs):
    return render_template(template, **kwargs, user=request.user)


@app.route('/')
def index():
    posts = Blog.select().join(User).order_by(Blog.id.desc())
    return render('blog.html', posts=posts)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render('register.html')
    else:
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        password = request.form['password']
        password_confirm = request.form['password_confirm']
        image = request.files.get('image')
        if password != password_confirm:
            return render('register.html', error='Пароли не совпадают')
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
            return render('register.html', error=error)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render('login.html')
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
                return render('login.html', error='Неверный пароль')
        else:
            return render('login.html', error='Пользователь не найден')


@app.route('/profile', methods=['GET'])
def profile():
    return render('profile.html')


@app.route('/edit_user', methods=['GET', 'POST'])
def edit_user():
    if request.method == 'GET':
        return render('edit_user.html')
    else:
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        password = request.form['password']
        password_confirm = request.form['password_confirm']
        image = request.files.get('image')
        if password != password_confirm:
            return render('register.html', error='Пароли не совпадают')
        if image and image.filename != '':
            filename = secure_filename(image.filename)
            image_path = 'media/' + filename
            image.save(image_path)
            request.user.image_path = image_path
    request.user.first_name = first_name
    request.user.last_name = last_name
    request.user.email = email
    request.user.password = password
    request.user.save()
    return redirect(url_for('profile'))


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
        tags = request.form['tags']
        tags_list = tags.split()
        images = request.files.getlist('files')

        blog = Blog.create(
            name=name,
            text=text,
            author=author,
        )

        for tag in tags_list:
            BlogTags.create(blog=blog, text=tag)

        print(images)
        for image in images:
            image.save('media/' + image.filename)
            image = 'media/' + image.filename
            BlogImage.create(
                blog=blog,
                image_path=image,
            )
        return redirect(url_for('index'))
    return render('add_post.html')


@app.route('/add_comment/<int:post_id>', methods=['POST'])
def add_comment(post_id):
    if request.method == 'POST':
        author = request.user.id
        text = request.form['text']

        Comment.create(
            blog_id=post_id,
            author=author,
            text=text,
        )
    return redirect(url_for('index'))


@app.route('/edit_post/<int:post_id>', methods=['GET', 'POST'])
def edit_post(post_id):
    post = Blog.get(Blog.id == post_id)
    if post.author != request.user:
        return redirect(url_for('login'))
    else:
        if request.method == 'GET':
            return render('edit_post.html')
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
    return render('post_detail.html', post=post)


@app.route('/media/<filename>')
def media(filename):
    return send_from_directory(directory=os.path.dirname('media/' + filename),
                               path=os.path.basename('media/' + filename))


if __name__ == '__main__':
    app.run(debug=True)
