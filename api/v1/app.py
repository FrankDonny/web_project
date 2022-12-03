#!/usr/bin/python3
"""the flask server app"""
from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views

app = Flask(__name__)
app.url_map.strict_slashes = False
app.register_blueprint(app_views)


@app.errorhandler(404)
def error_handler(error):
    """error handler method"""
    return jsonify({"error": "Not found"}), 404


@app.teardown_appcontext
def teardown(exception):
    """close a session"""
    storage.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, threaded=True, debug=True)