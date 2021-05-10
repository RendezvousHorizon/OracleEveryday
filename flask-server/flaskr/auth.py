import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.exceptions import abort

from .db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/register', methods=['POST'])
def register():
    error = None
    if request.method == 'POST':
        query_params = request.args
        username = query_params.get('username')
        password = query_params.get('password')
        db = get_db()

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif db.execute(
            'SELECT id FROM user WHERE username = ?', (username,)
        ).fetchone() is not None:
            error = 'User {} is already registered.'.format(username)

        if error is None:
            db.execute(
                'INSERT INTO user (username, password) VALUES (?, ?)',
                (username, generate_password_hash(password))
            )
            db.commit()
            return 'success'

    return error


@bp.route('/login', methods=['POST'])
def login():
    query_params = request.args
    username = query_params.get('username')
    password = query_params.get('password')
    db = get_db()
    error = None
    user = db.execute(
        'SELECT * FROM user WHERE username = ?', (username,)
    ).fetchone()

    if user is None:
        error = 'User {} does not exists.'.format(username)
    if not check_password_hash(user['password'], password):
        error = 'Incorrect username or password.'

    if error is None:
        session.clear()
        session['user_id'] = user['id']
        return 'success'

    else:
        return error


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()


@bp.route('/is_logged_in', methods=['GET'])
def is_logged_in():
    if g.user is not None:
        return 'logged in as {}'.format(g.user['username'])
    else:
        return 'not logged in'


@bp.route('/logout')
def logout():
    session.clear()
    return 'success'


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return abort(401, 'Login is required.')

        return view(**kwargs)

    return wrapped_view
