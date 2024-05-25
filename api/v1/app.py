#!/usr/bin/python3
"""Main module for the API"""
from flask import Flask
from flask import Blueprint
from flask import jsonify
from flask import make_response
from models import storage
from api.v1.views import app_views
import os


app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def close(err):
    storage.close()

@app.errorhandler(404)
def error_404(error):
    return make_response(jsonify({"error": "Not found"}))

if __name__ == "__main__":
    app.run(host=os.getenv("HBNB_API_HOST", "0.0.0.0"),
            port=int(os.getenv("HBNB_API_PORT", "5000")),
            threaded=True, debug=True)

    