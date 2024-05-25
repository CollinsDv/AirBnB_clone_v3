#!/usr/bin/python3

from flask import jsonify


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    from api.v1.views import app_views
    return jsonify({"status": "OK"})
