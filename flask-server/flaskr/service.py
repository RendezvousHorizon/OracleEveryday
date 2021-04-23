from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for,
    current_app, send_file, jsonify
)
from werkzeug.exceptions import abort
from werkzeug.utils import secure_filename
from .utils import recognize, image2base64

from .auth import login_required
from .db import get_db
import os

bp = Blueprint('service', __name__)


@bp.route('/oracle_recognition', methods=['GET'])
def oracle_recognition(api=False):
    image = request.files['image']
    image_name = secure_filename(image.filename)
    name = recognize(image)
    return name


@bp.route('/oracle_search', methods=['GET'])
def oracle_search(api=False):
    query_parameters = request.args
    name = query_parameters.get('name')

    db = get_db()
    result = db.execute(
        'SELECT * FROM oracle WHERE name="{}"'.format(name)
    ).fetchone()
    if result is None:
        abort(404, 'the oracle image of \'{}\' not found'.format(name))
    image_path = os.path.join(current_app.config['IMAGE_PATH'], result['img'])

    return send_file(image_path, mimetype='image/jpeg')


@bp.route('/wrong_question', methods=['POST'])
@login_required
def upload_wrong_question():
    query_parameters = request.args
    question_id = query_parameters.get('question_id')
    user_id = g.user['id']
    db = get_db()
    db.executescript('INSERT INTO wrong_question (user_id, question_id) VALUES ({}, {})'\
                     .format(user_id, question_id))
    return 'upload success'


@bp.route('/question', methods=['GET'])
def get_question():
    db = get_db()
    questions = db.execute('SELECT * FROM question LIMIT 10').fetchall()
    print('questions: ', questions)
    rv = []
    for q in questions:
        image_path = os.path.join(current_app.config['IMAGE_PATH'], q['img'])
        print(image_path)
        image_base64 = str(image2base64(image_path))
        tuple = {
            'id': q['id'],
            'image': image_base64,
            'a': q['a'],
            'b': q['b'],
            'c': q['c'],
            'd': q['d'],
        }
        rv.append(tuple)
    print(rv)
    return jsonify(rv)