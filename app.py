from flask import Flask, render_template, request, redirect, flash, jsonify, url_for
from flask_login import login_required, current_user, LoginManager, login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os
import re
from models import *
import time



def current_time():
    return int(time.time())


app = Flask(__name__, static_url_path='/static')
app.secret_key = os.urandom(24)

app.config['UPLOAD_FOLDER'] = 'static/media/avatars'
app.config['UPLOAD_FOLDER_POST'] = 'static/media/images_post'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def save_avatar(avatar):
    if avatar and allowed_file(avatar.filename):
        filename = secure_filename(avatar.filename)
        avatar.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return f'media/avatars/{filename}'  # Вернем путь к файлу для сохранения в базе данных
    else:
        return 'media/avatars/default_avatar.png'  # Возвращаем путь к дефолтной аватарке, если загрузка не удалась

def save_image_post(image):
    if image and allowed_file(image.filename):
        filename = secure_filename(image.filename)
        image.save(os.path.join(app.config['UPLOAD_FOLDER_POST'], filename))
        return f'media/images_post/{filename}'  
    else:
        return 'media/images_post/default_image.jpg'  
    

@login_manager.user_loader
def load_user(user_id):
    return Users.select().where(Users.id==int(user_id)).first()

@app.context_processor
def user_context_processor():
    return dict(user=current_user)


@app.before_request
def before_request():
    db.connect()

@app.after_request
def after_request(response):
    db.close()
    return response


#   ///////////////////////////  ВАЛИДАЦИЯ ПАРОЛЯ  /////////////////////////////



def validate_password(password):
    if len(password) < 8:
        return False
    if not re.search("[a-z]", password):
        return False
    if not re.search("[A-Z]", password):
        return False
    if not re.search("[0-9]", password):
        return False
    return True
    
    

#   ///////////////////////////  МАРШРУТИЗАТОРЫ  /////////////////////////////


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/gallery/')
@login_required
def gallery():
    all_posts = Posts.select()
    return render_template('gallery.html', posts=all_posts)

@app.route('/current_profile/')
@login_required
def current_profile():
    return render_template('profile.html')


@app.route('/profile/<int:id>/', methods=('GET', 'POST'))
def profile(id):
    profile_user = Users.select().where(Users.id == id).first()
    return render_template('profile.html', user=profile_user)


@app.route('/posts/', methods=['GET', 'POST'])
@login_required
def my_posts():
    all_posts = Posts.select().where(Posts.author == current_user)
    return render_template('gallery.html', posts=all_posts)


@app.route('/add_comment/<int:post_id>', methods=['POST'])
@login_required
def add_comment(post_id):
    post = Posts.select().where(Posts.id == post_id).first()
    content = request.json['content']
    if post:
        Comments.create(
            post=post,
            author=current_user,
            content=content
        )
        return jsonify(content=content, username=current_user.username)
    else:
        return jsonify(error="Post not found"), 404




@app.route('/post/<int:id>/', methods=['GET', 'POST'])
@login_required
def post_detail(id):
    post = Posts.select().where(Posts.id == id).first()
    if post:
        comments = Comments.select().where(Comments.post == post)
        return render_template('post.html', post=post, comments=comments, user=current_user)
    return f'Post with id = {id} does not exist'

 
@app.route('/<int:id>/setting/', methods=('GET', 'POST'))
@login_required
def update_profile(id):
    user = Users.select().where(Users.id == id).first()
    if request.method == "POST":
        if current_user==user:
            full_name = request.form['full_name']
            age = request.form['age']
            location = request.form['location']
            about_me = request.form['about_me']
            specialization = request.form['specialization']
            avatar = request.files['avatar']
            
            if location and location.strip() != '':
                user.location = location

            if full_name and full_name.strip() != '':
                user.full_name = full_name

            if about_me and about_me.strip() != '':
                user.about_me = about_me
            if specialization and specialization.strip() != '':
                user.specialization = specialization
            if age and age.strip() != '':
                user.age = age

            if avatar and avatar.filename != '':
                avatar_path = save_avatar(avatar)
                user.image = avatar_path

            user.save()
            return redirect('/current_profile/')
    return render_template('settings.html', user=current_user)




@app.route('/upload/', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == "POST":
        if 'title' in request.form and 'content' in request.form and 'image' in request.files:
            title = request.form['title']
            content = request.form['content']
            image = request.files['image']
            
            image_post_path = save_image_post(image) if image and allowed_file(image.filename) else 'media/images_post/default_image.jpg'
            
            Posts.create(
                title=title,
                author=current_user,
                content=content,
                image=image_post_path,
            )
            
            return redirect('/gallery')
        else:
            flash('Please fill all required fields and select a valid image file.')
    return render_template('create.html', user=current_user)      

@app.route('/post/<int:id>/update/', methods=('GET', 'POST'))
@login_required
def update(id):
    post = Posts.select().where(Posts.id==id).first()
    if request.method == "POST":
        if post:
            if current_user==post.author:

                title = request.form['title']
                content = request.form['content']
                image = request.files['image']

                if image and image.filename != '':
                    image_post_path = save_image_post(image)
                    post.image = image_post_path

                if title and title.strip() != '':
                    post.title = title

                if content and content.strip() != '':
                    post.content = content
                
                post.save()
                return redirect(f'/post/{id}/')
            return f'You are not author of this post'
        return f'Post with id = {id} does not exists'
    return render_template('update.html', post=post, user=current_user)


@app.route('/delete_post/<int:post_id>', methods=['POST'])
@login_required
def delete_post(post_id):
    post = Posts.get_or_none(Posts.id == post_id, Posts.author == current_user)
    if post:
        post.delete_instance()
        flash('Post deleted successfully.')
    else:
        flash('Post not found or permission denied.')
    return redirect(url_for('my_posts'))


@app.route('/signup', methods=['GET', 'POST'])
def register():
    if request.method=='POST':
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        user = Users.select().where(Users.email==email).first()
        if user:
            flash('Email address already exists')
            return redirect('/signup')
        if Users.select().where(Users.username==username).first():
            flash('Username already exists')
            return redirect('/signup')
        else:
            if validate_password(password):
                Users.create(
                    email=email,
                    username=username,
                    password=generate_password_hash(password)
                )
                return redirect('/login')
            else:
                flash('Wrong password')
                return redirect('/signup')
            
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    
    if request.method=='POST':
        email = request.form['email']
        password = request.form['password']
        user = Users.select().where(Users.email==email).first()
        if not user or not check_password_hash(user.password, password):
            flash('Please check you login details and try again.')
            return redirect('/login')  # Передайте оба параметра

        else:
            login_user(user)
            return redirect('/gallery/')
    return render_template('index.html')

@app.route('/logout/')
def logout():
    logout_user()
    return redirect('/')


#  //////////////////////////////////////  ЗАПУСК ПРОГРАММЫ  /////////////////////////////////////////


if __name__ == '__main__':
    app.run(debug=True)
