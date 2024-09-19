from flask import Blueprint, jsonify

users_blueprint = Blueprint('users', __name__, url_prefix='/users')


@users_blueprint.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify({
        'status': 'success',
        'message': 'pong!'
    })
