#!/usr/bin/python3
"""rooms api routes module"""
from flask import jsonify, abort, request
from models import storage
from api.v1.views import app_view
from models.rooms import Room
from datetime import datetime


@app_view.route("/rooms", methods=["GET"])
def get_rooms():
    """get the list of rooms"""
    return jsonify([obj.to_dict() for obj in storage.all("Room").values()]),\
        200


@app_view.route("/rooms/<room_id>", methods=["GET"])
def get_room(room_id):
    """get the room with the id passed"""
    id_list = [id_.split(".")[1] for id_ in storage.all("Room")]
    if room_id not in id_list:
        abort(404)
    obj = storage.get("Room", room_id)
    return jsonify(obj.to_dict()), 200  # type: ignore


@app_view.route("/rooms", methods=["POST"])
def create_room():
    """create a new room"""
    new_room = request.get_json(silent=True)
    if new_room is None:
        abort(400, description="Not a JSON")
    if "name" not in new_room.keys():
        return jsonify({"name": "name field is missing"}), 400
    if "description" not in new_room.keys():
        return jsonify({"description": "description field is missing"}), 400
    if "creator_id" not in new_room.keys():
        return jsonify({"creator_id": "creator_id field is missing"}), 400
    users_id = [obj.split(".")[1] for obj in storage.all("User").keys()]
    if new_room["creator_id"] not in users_id:
        abort(400, description="creator_id does not match any user")
    roomObj = Room(**new_room)
    storage.new(roomObj)
    storage.save()
    return jsonify(roomObj.to_dict()), 201


@app_view.route("/rooms/<room_id>", methods=["DELETE"])
def delete_room(room_id):
    """delete a room"""
    id_list = [id_.split(".")[1] for id_ in storage.all("Room")]
    if room_id not in id_list:
        abort(404)
    obj = storage.get("Room", room_id)
    storage.delete(obj)
    storage.save()
    return {}, 200


@app_view.route("/rooms/<room_id>", methods=["PUT"])
def update_room(room_id):
    """update a room"""
    id_list = [id_.split(".")[1] for id_ in storage.all("Room").keys()]
    if room_id not in id_list:
        abort(404)
    update = request.get_json(silent=True)
    if update is None:
        abort(400, description="Not a JSON")
    # if "name" not in update.keys() or "description" not in update.keys():
    #     abort(400, description="Only name and description can be updated")
    obj = storage.get("Room", room_id)
    for key, value in update.items():
        ls = ["name", "description"]
        if key not in ls:
            continue
        setattr(obj, key, value)
    setattr(obj, "updated_at", datetime.now())
    storage.save()
    return jsonify(obj.to_dict()), 200  # type: ignore
