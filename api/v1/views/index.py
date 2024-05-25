#!/usr/bin/python3
"""Index module for the API"""
from flask import jsonify
from models import storage
from api.v1.views import app_views
from models.state import State
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.user import User

classes = {"amenities": Amenity, "cities": City, "places": Place,
           "reviews": Review, "states": State, "users": User}


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    return jsonify({"status": "OK"})


@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def retrieve():
    """Retrieves the number of each objects by type"""

    items = {}
    for key, value in classes.items():
        items[key] = storage.count(value)

    return jsonify(items)
