#!/usr/bin/python3
"""users api routes module"""
from datetime import datetime

from flask import abort, jsonify, request

from api.v1.views import app_view
from models import storage
from models.users import User


@app_view.route("/users", methods=["GET"])
def get_users():
    """return all users"""
    return jsonify([obj.to_dict() for obj in storage.all("User").values()]),\
        200


@app_view.route("/users/<user_id>", methods=["GET"])
def get_user(user_id):
    """return a user based on the id"""
    id_list = [id_.split(".")[1] for id_ in storage.all("User").keys()]
    if user_id not in id_list:
        abort(404)
    obj = storage.get("User", user_id)
    return jsonify(obj.to_dict()), 200  # type: ignore


@app_view.route("/users", methods=["POST"])
def create_user():
    """create a new instance"""
    new_instance = request.get_json(silent=True)
    if new_instance is None:
        abort(400, description="Not a JSON")
    if "name" not in new_instance.keys():
        return jsonify({"name": "name field is missing"}), 400
    if "email" not in new_instance.keys():
        return jsonify({"email": "email field is missing"}), 400
    if "password" not in new_instance.keys():
        return jsonify({"password": "password field is missing"})
    new_user = User(**new_instance)
    storage.new(new_user)
    storage.save()
    return jsonify({"newUser": new_user.to_dict()}), 201


@app_view.route("/users/<user_id>", methods=["DELETE"])
def delete_user(user_id):
    """delete an instance of User"""
    id_list = [id_.split(".")[1] for id_ in storage.all("User").keys()]
    if user_id not in id_list:
        abort(404)
    obj = storage.get("User", user_id)
    storage.delete(obj)
    storage.save()
    return {}, 200


@app_view.route("/users/<user_id>", methods=["PUT"])
def update_user(user_id):
    """update an instance of User"""
    id_list = [id_.split(".")[1] for id_ in storage.all("User").keys()]
    if user_id not in id_list:
        abort(404)
    obj = storage.get("User", user_id)
    update = request.get_json(silent=True)
    if update is None:
        abort(404, description="Not a JSON")
    for key, value in update.items():
        ls = ["name", "email", "password", "number"]
        if key not in ls:
            continue
        setattr(obj, key, value)
    setattr(obj, "updated_at", datetime.now())
    storage.save()
    return jsonify({"updated": obj.to_dict()}), 200  # type: ignore
