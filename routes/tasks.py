from flask import request, jsonify, Blueprint
from db import get_collection
from bson import ObjectId

tasks_bp = Blueprint("tasks", __name__)

@tasks_bp.route("/tasks", methods=["GET"])
def get_tasks():
    col = get_collection("todo")
    db_tasks = list(col.find())
    for task in db_tasks:
        task["_id"] = str(task["_id"])
    return jsonify({"success": True, "data": db_tasks})

@tasks_bp.route("/tasks", methods=["POST"])
def create_task():
    data = request.get_json(silent=True)
    new_task = {
        "title": data.get("title", "Untitled").strip(),
        "body": data.get("body", "").strip(),
        "priority": int(data.get("priority", 1)),
        "completed": False,
        "subtasks": data.get("subtasks", []) # שמירת תתי המשימות
    }
    col = get_collection("todo")
    col.insert_one(new_task)
    new_task["_id"] = str(new_task["_id"])
    return jsonify({"success": True, "data": new_task}), 201

@tasks_bp.route("/tasks/<task_id>", methods=["PUT"])
def update_task(task_id):
    data = request.get_json(silent=True)
    col = get_collection("todo")
    # מעדכן רק מה שנשלח
    col.update_one({"_id": ObjectId(task_id)}, {"$set": data})
    return jsonify({"success": True})

@tasks_bp.route("/tasks/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    col = get_collection("todo")
    col.delete_one({"_id": ObjectId(task_id)})
    return jsonify({"success": True})

@tasks_bp.route("/tasks/<task_id>", methods=["GET"])
def get_single_task(task_id):
    col = get_collection("todo")
    task = col.find_one({"_id": ObjectId(task_id)})
    if task:
        task["_id"] = str(task["_id"])
    return jsonify({"success": True, "data": task})