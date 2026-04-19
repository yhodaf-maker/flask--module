from flask import request, jsonify, Blueprint
from werkzeug.exceptions import NotFound, BadRequest, Conflict, UnprocessableEntity
from models import tasks
from db import db
from bson import ObjectId

tasks_bp = Blueprint("tasks", __name__)


@tasks_bp.route("/tasks", methods=["GET"])
def get_tasks():
    # Return every task currently stored in memory.
    db_tasks = list(db.todo.find())
    for task in db_tasks:
        task["_id"] = str(task["_id"])
    return jsonify({
        "success": True,
        "data": db_tasks
    })



@tasks_bp.route("/tasks/<task_id>", methods=["GET"])
def get_task(task_id):
    # Look up a single task and fail with 404 if it does not exist.
    task = db.todo.find_one({"_id": task_id})
    if not task:
        raise NotFound(f"{task_id} not found")
    task["_id"] = str(task["_id"])
    return jsonify({
        "success": True,
        "data": task
    })


@tasks_bp.route("/tasks", methods=["POST"])
def create_task():
    # `silent=True` lets us raise our own JSON-friendly validation error.
    data = request.get_json(silent=True)
    if not data or not isinstance(data, dict):
        raise BadRequest("request body must be json")
    if "title" not in data:
        raise BadRequest("title is required")
    title = data["title"]
    if not isinstance(title, str):
        raise BadRequest("title must be a string")
    if not title.strip():
        raise UnprocessableEntity("title must contain text")

    # New tasks get a generated id and start as incomplete.
    new_task = {
        "title": title.strip(),
        "completed": False  
    }
    
    db.todo.insert_one(new_task)
    new_task["_id"] = str(new_task["_id"])
    return jsonify({
        "success": True,
        "data": new_task
    }), 201


@tasks_bp.route("/tasks/<task_id>", methods=["PUT"])
def change_task(task_id):

    data = request.get_json(silent=True)

    if not data or not isinstance(data, dict):
        raise BadRequest("request must contain json")

    update_data = {}

    if "title" in data:
        if not isinstance(data["title"], str):
            raise BadRequest("title must be a string")
        if not data["title"].strip():
            raise UnprocessableEntity("title must contain text")
        update_data["title"] = data["title"].strip()

    if "completed" in data:
        if not isinstance(data["completed"], bool):
            raise BadRequest("completed must be boolean")
        update_data["completed"] = data["completed"]

    result = db.todo.update_one(
        {"_id": ObjectId(task_id)},   # 🔥 זה התיקון החשוב
        {"$set": update_data}
    )

    if result.matched_count == 0:
        raise NotFound(f"{task_id} not found")

    updated_task = db.todo.find_one({"_id": ObjectId(task_id)})
    updated_task["_id"] = str(updated_task["_id"])

    return jsonify({
        "success": True,
        "data": updated_task
    })
    
@tasks_bp.route("/tasks/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    # Delete the matching task and confirm which one was removed.
    result = db.todo.delete_one({"_id": ObjectId(task_id)})
    if result.deleted_count == 0:
        raise NotFound(f"{task_id} not found")
    return jsonify({
        "success": True,
        "message": f"removed task {task_id}"
    }), 200
    
