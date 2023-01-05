#!/usr/bin/python3
from flask import Flask, jsonify
from views import app_view

api_app = Flask(__name__)
api_app.url_map.strict_slashes = False
api_app.register_blueprint(app_view)


@api_app.errorhandler(404)
def error_handler(error):
    """handles all error"""
    return jsonify({"Error": "Not found"})


@api_app.teardown_appcontext
def close_(close):
    """closes a session"""
    from models import storage
    storage.close()


if __name__ == "__main__":
    api_app.run(host="0.0.0.0", port=5001, debug=True)
