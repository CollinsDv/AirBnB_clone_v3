#!/usr/bin/python3
"""Cities module for the API"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities',
                 methods=['GET'], strict_slashes=False)
def amenities():
    amenitys = storage.all(Amenity)
    return jsonify([amenity.to_dict() for amenity in amenitys])


@app_views.route('/amenities/<amenity_id>',
                 methods=['GET'], strict_slashes=False)
def amenity_object(city_id):
    amenity = storage.get(Amenity, city_id)
    if amenity is None:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route('/amenities',
                 methods=['POST'], strict_slashes=False)
def amenity_create():
    data = request.get_json()
    if not data:
        abort(400, description="Not a JSON")
    if 'name' not in data:
        abort(400, description="Missing name")
    amenity = Amenity(**data)
    storage.new(amenity)
    storage.save()
    return jsonify(amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>',
                 methods=['PUT'], strict_slashes=False)
def amenity_update(amenity_id):
    data = request.get_json()
    if not data:
        abort(400, description="Not a JSON")
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(amenity, key, value)
    storage.save()
    return jsonify(amenity.to_dict()), 200
