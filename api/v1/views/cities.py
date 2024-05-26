#!/usr/bin/python3
"""Cities module for the API"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.state import State
from models.city import City


@app_views.route('/states/<state_id>/cities',
                 methods=['GET'], strict_slashes=False)
def cities(state_id):
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    return jsonify([city.to_dict() for city in state.cities])


@app_views.route('/api/v1/cities/<city_id>',
                 methods=['GET'], strict_slashes=False)
def city_object(city_id):
    city = storage.get(City, city_id)
    return city
    # if city is None:
    #     abort(404)
    # return jsonify(city.to_dict())


@app_views.route('/api/v1/cities/<city_id>',
                 methods=['DELETE'], strict_slashes=False)
def city_delete(city_id):
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    storage.delete(city)
    storage.save()
    return jsonify({}), 200


@app_views.route('/api/v1/states/<state_id>/cities',
                 methods=['POST'], strict_slashes=False)
def city_create(state_id):
    data = request.get_json()
    if not data:
        abort(400, description="Not a JSON")
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    if 'name' not in data:
        abort(400, description="Missing name")
    city = City(**data)
    city.state_id = state_id
    storage.new(city)
    storage.save()
    return jsonify(city.to_dict()), 201


@app_views.route('/api/v1/cities/<city_id>',
                 methods=['PUT'], strict_slashes=False)
def city_update(city_id):
    data = request.get_json()
    if not data:
        abort(400, description="Not a JSON")
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    city = City(**data)
    storage.save()
    return jsonify(city.to_dict()), 200
