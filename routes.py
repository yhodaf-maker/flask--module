from flask import request, jsonify, Blueprint
from werkzeug.exceptions import NotFound, BadRequest, Conflict, UnprocessableEntity
from models import tasks
import uuid


tasks_bp = Blueprint("tasks", __name__)


@tasks_bp.route("/tasks", methods=["GET"])
def get_tasks():
    # Return every task currently stored in memory.
    return tasks


@tasks_bp.route("/tasks/<task_id>", methods=["GET"])
def get_task(task_id):
    # Look up a single task and fail with 404 if it does not exist.
    for task in tasks:
        if task_id == task["id"]:
             return task
    raise NotFound(f"{task_id} not found")


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
    "id": str(uuid.uuid4()),
    "title": title.strip(),
    "completed": False
        }
    tasks.append(new_task)
    return jsonify({
        "success": True,
        "data": new_task
    }), 201


@tasks_bp.route("/tasks/<task_id>", methods=["PUT"])
def change_task(task_id):
    # Updates accept only the fields this simple API knows how to change.
    data = request.get_json(silent=True)
    if not data or not isinstance(data, dict):
        raise BadRequest("error: update request must contain data")
    keys = ("title", "completed")
    data_keys = data.keys()
    for key in data_keys:
        if key not in keys:
            raise BadRequest(f"not allowed to pass {key}")
    for task in tasks:
            if task_id == task["id"]:
                if "title" in data:
                    if not isinstance(data["title"], str):
                        raise BadRequest("title must be a string")
                    if not data["title"].strip():
                        raise UnprocessableEntity("title must contain text")
                    # Trim whitespace so stored titles stay clean.
                    task["title"] = data["title"].strip()
                if "completed" in data:
                    if not isinstance(data["completed"], bool):
                        raise BadRequest("completed must be a boolean")
                    task["completed"] = data["completed"]
                return task
    raise NotFound(f"{task_id} not found")


@tasks_bp.route("/tasks/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    # Delete the matching task and confirm which one was removed.
    for task in tasks:
        if task["id"] == task_id:
            tasks.remove(task)

            return {
                "Message": f"removed task {task['title']}"
            }
    raise NotFound(f"{task_id} not found")