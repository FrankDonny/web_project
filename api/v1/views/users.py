#!/usr/bin/python3
"""This module handles default users requests"""
from flask import abort, request, jsonify
from api.v1.views import app_views


@app_views.route("/users", methods=["GET"])
def get_users():
    """get list of all users"""
    from models import storage
    return jsonify([obj.to_dict() for obj in storage.all("User").values()])