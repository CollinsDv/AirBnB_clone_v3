#!/usr/bin/python3
from models import user
from models import storage
from api.v1.views import app_views
from flask import jsonify, abort, request


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_user():
    """gets all users"""
    users = storage.all(user)
    return jsonify(users)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_user_id(user_id):
    """gets user by id"""
    user = storage.get(user, user_id)
    if user is None:
        abort(404)
    return jsonify(user)


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    """deletes user by id"""
    user = storage.get(user, user_id)
    if user is None:
        abort(404)
    storage.delete(user)
    storage.save()
    return jsonify({}), 200


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def post_user():
    """creates a user"""
    if not request.get_json():
        abort(400, 'Not a JSON')
    if 'email' not in request.get_json():
        abort(400, 'Missing email')
    if 'password' not in request.get_json():
        abort(400, 'Missing password')

    new_user = user(**request.get_json())
    storage.new(new_user)
    storage.save()

    response = jsonify(new_user.to_dict())
    response.status_code = 201
    return response


@app_views.route('/user/<user_id>', methods=['PUT'], strict_slashes=False)
def put_user(user_id):
    """updates user by id"""
    user = storage.get(user, user_id)
    if user is None:
        abort(404)
    if not request.get_json():
        abort(400, 'Not a JSON')
    for key, value in request.get_json().items():
        if key not in ['id', 'email', 'created_at', 'updated_at']:
            setattr(user, key, value)
    storage.save()
    return jsonify(user), 200
