#!/usr/bin/python3
"""Module for the state API"""
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from flask import jsonify, make_response, abort, request


@app_views.route('/amenities',
                 methods=['GET'], strict_slashes=False)
def get_amenities():
    """Retrieves amenities objects"""
    amenity_list = [amenity.to_dict() for amenity in storage.all(
        Amenity).values()]
    return jsonify(amenity_list)


@app_views.route('/amenities/<amenity_id>',
                 methods=['GET'], strict_slashes=False)
def get_amenity_id(amenity_id):
    """get an amenity by id"""
    amenity_obj = storage.get(Amenity, amenity_id)
    if amenity_obj:
        return jsonify(amenity_obj.to_dict())
    abort(404)


@app_views.route('/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_amenity(amenity_id):
    """deletes a state with state_id"""
    obj = storage.get(Amenity, amenity_id)
    if obj:
        storage.delete(obj)
        storage.save()
        return jsonify({}), 200
    abort(404)


@app_views.route('/amenities',
                 methods=['POST'], strict_slashes=False)
def add_amenity():
    """add a new state"""
    request_data = request.get_json()
    if not request_data:
        abort(400, description='Not a JSON')
    if 'name' not in request_data:
        abort(400, description='Missing name')

    new_amenity = Amenity(**request_data)
    storage.new(new_amenity)
    storage.save()

    response = jsonify(new_amenity.to_dict())
    response.status_code = 201
    return response


@app_views.route('/amenities/<amenity_id>',
                 methods=['PUT'], strict_slashes=False)
def update_amenity(amenity_id):
    """update a state by ID"""
    amenity_obj = storage.get(Amenity, amenity_id)
    if not amenity_obj:
        abort(404)
    request_data = request.get_json()
    if not request_data:
        abort(400, description="Not a JSON")

    for key, value in request_data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(amenity_obj, key, value)
    storage.save()

    return jsonify(amenity_obj.to_dict()), 200


@app_views.errorhandler(404)
def handle_err_404(error):
    """handle 404 error"""
    return make_response(jsonify({"error": "Not found"}), 404)


@app_views.errorhandler(400)
def handle_err_400(error):
    """handle 400 error"""
    return make_response(jsonify(
                                 {"error": error.description}), 400)
