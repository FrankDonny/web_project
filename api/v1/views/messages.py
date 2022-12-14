#!/usr/bin/python3
"""messages api routes module"""
from datetime import datetime

from flask import abort, jsonify, request

from api.v1.views import app_view
from models import storage
from models.messages import Message
from models.rooms import Room


@app_view.route("/messages", methods=["GET"])
def get_messages():
    """get list of all messages"""
    return jsonify([obj.to_dict() for obj in storage.all("Message").values()])


@app_view.route("/messages/<message_id>", methods=["GET"])
def get_message(message_id):
    """get a message"""
    id_list = [key.split(".")[1] for key in storage.all("Review").keys()]
    if message_id not in id_list:
        abort(404)
    obj = storage.get("Message", message_id)
    return jsonify(obj.to_dict()), 200  # type: ignore


@app_view.route("/messages", methods=["POST"])
def create_message():
    """create a new message"""
    new_message = request.get_json(silent=True)
    if new_message is None:
        abort(400, description="Not a JSON")
    if "text" not in new_message.keys():
        abort(400, description="text field is missing")
    if "user_id" not in new_message.keys():
        abort(400, description="user_id field is missing")
    if "room_id" not in new_message.keys():
        abort(400, description="room_id field is missing")
    users_id = [key.split(".")[1] for key in storage.all("User").keys()]
    if new_message["user_id"] not in users_id:
        abort(400, description="user_id does not match any user")
    rooms_id = [key.split(".")[1] for key in storage.all("Room").keys()]
    if new_message["room_id"] not in rooms_id:
        abort(400, description="room_id does not match any Room")
    new_instance = Message(**new_message)
    storage.new(new_instance)
    storage.save()
    return jsonify(new_instance.to_dict()), 201


@app_view.route("/messages/<message_id>", methods=["DELETE"])
def delete_message(message_id):
    """delete a message instance"""
    id_list = [key.split(".")[1] for key in storage.all("Review").keys()]
    if message_id not in id_list:
        abort(404)
    obj = storage.get("Message", message_id)
    storage.delete(obj)
    storage.save()
    return {}


@app_view.route("/messages/<message_id>", methods=["PUT"])
def update_message(message_id):
    """update a message"""
    id_list = [key.split(".")[1] for key in storage.all("Message").keys()]
    if message_id not in id_list:
        abort(404)
    update = request.get_json(silent=True)
    if update is None:
        abort(400, description="Not a JSON")
    updateObject = storage.get("Message", message_id)
    for key, value in update.items():
        if key != "text":
            continue
        setattr(updateObject, key, value)
    setattr(updateObject, "updated_at", datetime.now())
    storage.save()
    return jsonify(updateObject.to_dict())  # type: ignore
