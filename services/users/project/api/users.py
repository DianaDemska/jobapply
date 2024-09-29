from flask import Blueprint, jsonify, request
from project import db
from .models import User

users_blueprint = Blueprint('users', __name__, url_prefix='/users')


@users_blueprint.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify({
        'status': 'success',
        'message': 'pong!'
    })


@users_blueprint.route('/', methods=['POST'])
def add_user():
    response = response_gen('fail', 'Invalid payload.', status_code=400)
    username = request.form.get('username')
    email = request.form.get('email')

    if not username or not email:
        return response

    try:
        user = User.query.filter_by(email=email).first()
        if not user:
            db.session.add(User(username=username, email=email))
            db.session.commit()
        else:
            response = response_gen(
                'fail', 'Email already exist.', status_code=400)
            return response
    except db.IntegrityError:
        db.session.rollback()
        return response

    response = response_gen(message=f'{username} was added.', status_code=201)
    return response


@users_blueprint.route('/<int:user_id>', methods=['GET'])
def get_user(user_id):
    response = response_gen('fail', 'User was not found.', status_code=404)
    try:
        user = User.query.filter_by(id=user_id).first()
        if not user:
            return response
    except ValueError:
        return response

    response = response_gen(user=user)
    return response


@users_blueprint.route('/', methods=['GET'])
def get_users():
    users = User.query.all()
    response = response_gen(users=users)
    return response


def response_gen(
        status='success',
        message=None,
        user=None,
        users=None,
        status_code=200):
    response_obj = {
        'status': status,
        'message': message,
        'data': {}
    }

    if user:
        response_obj['data']['user'] = user.to_json()
    if users:
        response_obj['data']['users'] = [usr.to_json() for usr in users]
    return jsonify(response_obj), status_code
