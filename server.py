import os

import timeago, datetime

from flask import Flask, render_template, session, request, url_for, redirect

from database import database
from user import user
from slider import slider
from posts import posts
from post import post

from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'F12Zr47j\3yX R~X@H!jmM]Lwf/,?KT'

allowed_image_extensions = [".png", ".jpg", ".jpeg"]

db = database()


@app.route('/')
def home():
    db.connect()

    carousel = slider(db)
    ps = posts(db)

    if session.get('authenticated'):
        client = user(session['user_id'], db)
    else:
        client = None

    return render_template('home.html', page_title='gusty.bike', client=client, carousel=carousel,
                           ago=timeago,date=datetime, recent_posts=ps.most_recent())


@app.route('/login')
def login():

    if session.get('authenticated'):
        return redirect(url_for('home'))

    return render_template('login.html', page_title='gusty.bike', client=None)


@app.route('/logout')
def logout():
    if session.get('authenticated'):
        session.clear()

    return redirect(url_for('home'))


@app.route('/about')
def about():
    db.connect()

    if session.get('authenticated'):
        client = user(session['user_id'], db)
    else:
        client = None

    return render_template('about.html', page_title='gusty.bike', client=client)


@app.route('/contests')
def contests():
    db.connect()

    if session.get('authenticated'):
        client = user(session['user_id'], db)
    else:
        client = None

    return render_template('contests.html', page_title='gusty.bike', client=client)


@app.route('/authenticate', methods=['GET', 'POST'])
def authenticate():
    if request.method == "POST":

        db.connect()

        request_type = request.form["type"]

        if request_type == "l":
            if not request.form["username"] or not request.form["password"]:
                return '2'  # response 2 = field blank

            username = request.form["username"]
            password = request.form["password"]

            uid = user.login(username, password, db)

            if uid == 0:
                return '0'  # response 0 = fail
            else:
                session['user_id'] = uid
                session['authenticated'] = True

                return '1'  # response 1 = SUCCESS!

        if request_type == "r":
            if not request.form["username"] or not request.form["email"] or \
                    not request.form["password"] or not request.form["password2"]:
                return '2'  # response 2 = field blank

            username = request.form["username"]
            email = request.form["email"]
            password = request.form["password"]
            password2 = request.form["password2"]

            if '@' not in email or '.' not in email:
                return '3'  # response 3 = email not formatted correctly

            if password != password2:
                return '4'  # response 4 = passwords do not match

            if not len(password) >= 6:
                return '5'  # response 5 = password not long enough

            if not username.isalnum() or len(username) >= 30:
                return '6'  # response 6 = username does not fit criteria

            if user.exists(username, db):
                return '0'  # response 7 user already exists

            session['user_id'] = user.create(email, password, username, db)

            #print(session['user_id'])

            #session['authenticated'] = True

            return '1'  # response 1 = SUCCESS!
    else:
        return None  # return nothing because the request isnt valid


@app.route('/admin/users/authenticate', methods = ['GET', 'POST'])
def register_user():
    if request.method == "POST":

        db.connect()

        request_type = request.form["type"]

        if request_type == "l":
            if not request.form["username"] or not request.form["password"]:
                return '2'  # response 2 = field blank

            username = request.form["username"]
            password = request.form["password"]

            uid = user.login(username, password, db)

            if uid == 0:
                return '0'  # response 0 = fail
            else:
                session['user_id'] = uid
                session['authenticated'] = True

                return '1'  # response 1 = SUCCESS!

        if request_type == "r":
            if not request.form["username"] or not request.form["email"] or \
                    not request.form["password"] or not request.form["password2"]:
                return '2'  # response 2 = field blank

            username = request.form["username"]
            email = request.form["email"]
            password = request.form["password"]
            password2 = request.form["password2"]

            if '@' not in email or '.' not in email:
                return '3'  # response 3 = email not formatted correctly

            if password != password2:
                return '4'  # response 4 = passwords do not match

            if not len(password) >= 6:
                return '5'  # response 5 = password not long enough

            if not username.isalnum() or len(username) >= 30:
                return '6'  # response 6 = username does not fit criteria

            if user.exists(username, db):
                return '0'  # response 7 user already exists

            session['user_id'] = user.create(email, password, username, db)

            #print(session['user_id'])

            #session['authenticated'] = True

            return '1'  # response 1 = SUCCESS!
    else:
        return None  # return nothing because the request isnt valid


@app.route('/post/<id>')
def view_post(id):
    db.connect()

    p = post(db, id)
    ps = posts(db)

    if session.get('authenticated'):
        client = user(session['user_id'], db)
    else:
        client = None

    return render_template('post.html', page_title='gusty.bike', p=p, client=client, ago=timeago,
                           date=datetime, recent_posts=ps.most_recent(p.id))


@app.route('/admin')
def admin():

    if not session.get('authenticated'):
        return redirect(url_for('home'))

    db.connect()

    client = user(session['user_id'], db)

    if not admin_check():
        return redirect(url_for('home'))

    return render_template('admin.html', page_title='gusty.bike', client=client)


@app.route('/admin/sliders/new')
def new_slider():
    if not session.get('authenticated'):
        return redirect(url_for('home'))

    db.connect()

    client = user(session['user_id'], db)

    if not admin_check():
        return redirect(url_for('home'))

    return render_template('admin_sliders_new.html', page_title='gusty.bike', client=client)


@app.route('/admin/posts/new')
def new_post():
    if not session.get('authenticated'):
        return redirect(url_for('home'))

    db.connect()
    client = user(session['user_id'], db)

    if not admin_check():
        return redirect(url_for('home'))

    return render_template('admin_posts_new.html', page_title='gusty.bike', client=client)


@app.route('/admin/users/new')
def new_user():
    if not session.get('authenticated'):
        return redirect(url_for('home'))

    db.connect()
    client = user(session['user_id'], db)

    if not admin_check():
        return redirect(url_for('home'))

    return render_template('admin_users_new.html', page_title='gusty.bike', client=client)


@app.route('/admin/api/sliders/new', methods=['GET', 'POST'])
def admin_api_new_slider():

    if not admin_check():
        return '0'  # not an admin

    if not request.method == "POST":
        return '0'

    f = request.files["sliderImage"]
    order = request.form["order"]

    if order is None or len(order) == 0:
        order = '#'  # user doesn't care about the order

    if not isinstance(order, int) and not order == "#":
        return '2'  # response 2 order not a number

    if f and is_image(f.filename):
        path = os.path.join("./static/slider_images/", secure_filename(f.filename))

        f.save(path)

        carousel = slider(db)

        if order == "#":
            carousel.upload(path, 0)
        else:
            carousel.upload(path, order)

        return '1'  # response 1 success

    return '0'  # response 0 uncaught error/type is incorrect


@app.route('/admin/api/posts/new', methods=['POST'])
def admin_api_new_post():
    if not admin_check():
        return "admin_fail"

    if not request.method == "POST":
        return None

    title = request.form["title"]
    content = request.form["safe_content"]

    if title is None:
        return "title_fail"

    if content is None:
        return "content_fail"

    author_id = session["user_id"]

    if "newPostImage" in request.files:
        f = request.files["newPostImage"]

        if f and is_image(f.filename):
            path = os.path.join("./static/post_images/", secure_filename(f.filename))
            f.save(path)

            return str(post.create(db, title, content, author_id, path))

    return str(post.create(db, title, content, author_id, " "))


def is_image(file):
    for ext in allowed_image_extensions:
        if file.endswith(ext):
            return True

    return False


def admin_check():
    if not session.get('authenticated'):
        return False

    db.connect()

    client = user(session['user_id'], db)

    if not client.admin == 1:
        return False

    return True


# start the server
if __name__ == '__main__':
    app.run(debug=True)
