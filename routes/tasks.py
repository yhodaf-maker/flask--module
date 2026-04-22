from flask import request, jsonify, Blueprint
from werkzeug.exceptions import NotFound, BadRequest, UnprocessableEntity
from bson import ObjectId
from db import get_collection
from models.tasks import format_task, create_task_model

tasks_bp = Blueprint("tasks", __name__)

# Fetch all tasks
@tasks_bp.route("/tasks", methods=["GET"])
def get_tasks():
    col = get_collection("todo")
    db_tasks = list(col.find())
    return jsonify({
        "success": True,
        "data": [format_task(task) for task in db_tasks]
    })

# Create a new task with priority
@tasks_bp.route("/tasks", methods=["POST"])
def create_task():
    data = request.get_json(silent=True)
    if not data or "title" not in data:
        raise BadRequest("title is required")
    
    # Extract priority from request, default to 1 (Low)
    priority = data.get("priority", 1)
    new_task = create_task_model(data["title"], data.get("body", ""), priority)
    
    col = get_collection("todo")
    col.insert_one(new_task)
    return jsonify({"success": True, "data": format_task(new_task)}), 201

# Update an existing task (including title, body, completed, and priority)
@tasks_bp.route("/tasks/<task_id>", methods=["PUT"])
def change_task(task_id):
    try:
        obj_id = ObjectId(task_id)
    except Exception:
        raise BadRequest(f"{task_id} is not a valid id")
    
    data = request.get_json(silent=True)
    update_data = {}

    if "title" in data: update_data["title"] = data["title"].strip()
    if "body" in data: update_data["body"] = data["body"].strip()
    if "completed" in data: update_data["completed"] = bool(data["completed"])
    if "priority" in data: update_data["priority"] = data["priority"]

    col = get_collection("todo")
    result = col.update_one({"_id": obj_id}, {"$set": update_data})
    
    if result.matched_count == 0:
        raise NotFound(f"{task_id} not found")

    updated_task = col.find_one({"_id": obj_id})
    return jsonify({"success": True, "data": format_task(updated_task)})

# Delete a task
@tasks_bp.route("/tasks/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    col = get_collection("todo")
    result = col.delete_one({"_id": ObjectId(task_id)})
    if result.deleted_count == 0:
        raise NotFound(f"{task_id} not found")
    return jsonify({"success": True, "message": "Task removed"}), 200