#!/usr/bin/python3
"""reviews api routes module"""
from datetime import datetime

from flask import abort, jsonify, request

from api.v1.views import app_view
from models import storage
from models.reviews import Review


@app_view.route("/reviews", methods=["GET"])
def get_reviews():
    """get list of reviews"""
    return jsonify([obj.to_dict() for obj in storage.all("Review").values()]),\
        200


@app_view.route("/reviews/<review_id>", methods=["GET"])
def get_review(review_id):
    """get a review"""
    id_list = [key.split(".")[1] for key in storage.all("Review").keys()]
    if review_id not in id_list:
        abort(404)
    obj = storage.get("Review", review_id)
    return jsonify(obj.to_dict()), 200  # type: ignore


@app_view.route("/reviews", methods=["POST"])
def create_review():
    """create a new review"""
    new_review = request.get_json(silent=True)
    if new_review is None:
        abort(400, description="Not a JSON")
    if "text" not in new_review.keys():
        abort(400, description="text field missing")
    if "user_id" not in new_review.keys():
        abort(400, description="user_id field missing")
    users_id = [key.split(".")[1] for key in storage.all("User").keys()]
    if new_review["user_id"] not in users_id:
        abort(400, description="user_id does not match any user")
    obj = Review(**new_review)
    storage.new(obj)
    storage.save()
    return jsonify(obj.to_dict()), 201


@app_view.route("/reviews/<review_id>", methods=["DELETE"])
def delete_review(review_id):
    """delete a review instance"""
    id_list = [key.split(".")[1] for key in storage.all("Review").keys()]
    if review_id not in id_list:
        abort(404)
    obj = storage.get("Review", review_id)
    storage.delete(obj)
    storage.save()
    return {}, 200


@app_view.route("/reviews/<review_id>", methods=["PUT"])
def update_review(review_id):
    """update a review instance"""
    review_ids = [key.split(".")[1] for key in storage.all("Review").keys()]
    if review_id not in review_ids:
        abort(404)
    update = request.get_json(silent=True)
    if update is None:
        abort(400, description="Not a JSON")
    review_instance = storage.get("Review", review_id)
    for key, value in update.items():
        if key != "text":
            continue
        setattr(review_instance, key, value)
    setattr(review_instance, "updated_at", datetime.now())
    storage.save()
    return jsonify({"updated": review_instance.to_dict()}), 200  # type: ignore
