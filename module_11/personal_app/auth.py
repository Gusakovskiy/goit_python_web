import functools
from random import choice
from string import hexdigits

from bson.objectid import ObjectId
from flask import (
    Blueprint,
    flash,
    g,
    redirect,
    render_template, request, session, url_for
)
from pymongo.collection import Collection
from werkzeug.security import check_password_hash, generate_password_hash

from .db import get_db

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


def _get_random_str(number_ch=10):
    return ''.join(choice(hexdigits) for _ in range(number_ch))


def _example_todos():
    return [
        dict(title='Register in App', done=True, priority=0),
        dict(title='Plan next week', done=False, description='You doing great', priority=1),
        dict(
            title='Sleep more well',
            done=False,
            description='Sleep is very important for your health',
            priority=3,
        ),
        dict(
            title='Buy healthy food', done=False, priority=4),
    ]


@auth_bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'

        if username:
            user = db.user.find_one(
                {"username": username}
            )
            if user is not None:
                error = 'Already registered.'

        if error is None:
            collection_name = f'todo_list_{username}_{_get_random_str()}'
            db.user.insert_one(
                dict(
                    username=username,
                    password=generate_password_hash(password),
                    todo_collection=collection_name
                ),
            )
            user_todo: Collection = getattr(db, collection_name)
            user_todo.insert_many(_example_todos())

            return redirect(url_for("auth.login"))

        flash(error)

    return render_template('auth/register.html')


@auth_bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.user.find_one(
            {"username": username}
        )

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = str(user['_id'])
            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login.html')


@auth_bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        db = get_db()
        g.user = db.user.find_one(
            {"_id": ObjectId(user_id)}
        )


@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)
    return wrapped_view
