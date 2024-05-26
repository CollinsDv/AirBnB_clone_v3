#!/usr/bin/python3
"""Module for the state API"""
from api.v1.views import app_views
from models import storage
from models.state import State
from flask import jsonify, make_response, abort, request


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    """Retrieves a state objects"""
    state_list = [state.to_dict() for state in storage.all(State).values()]
    return jsonify(state_list)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state_id(state_id):
    """get a state by id"""
    state_obj = storage.get(State, state_id)
    if state_obj:
        return jsonify(state_obj.to_dict())
    abort(404)


@app_views.route('/states/<state_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_state(state_id):
    """deletes a state with state_id"""
    obj = storage.get(State, state_id)
    if obj:
        storage.delete(obj)
        storage.save()
        return jsonify({}), 200
    abort(404)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def add_state():
    """add a new state"""
    request_data = request.get_json()
    if not request_data:
        abort(400, description='Not a JSON')
    if 'name' not in request_data:
        abort(400, description='Missing name')

    new_state = State(**request_data)
    storage.new(new_state)
    storage.save()

    response = jsonify(new_state.to_dict())
    response.status_code = 201
    return response


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """update a state by ID"""
    state_obj = storage.get(State, state_id)
    if not state_obj:
        abort(404)
    request_data = request.get_json()
    if not request_data:
        abort(400, description="Not a JSON")

    for key, value in request_data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            # state_obj.__dict__[key] = value
            setattr(state_obj, key, value)
    storage.save()

    return jsonify(state_obj.to_dict()), 200


@app_views.errorhandler(404)
def handle_err_404(error):
    """handle 404 error"""
    return make_response(jsonify({"error": "Not found"}), 404)


@app_views.errorhandler(400)
def handle_err_400(error):
    """handle 400 error"""
    return make_response(jsonify(
                                 {"error": error.description}), 400)
