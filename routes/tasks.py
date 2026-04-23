from flask import request, jsonify, Blueprint
from db import get_collection
from bson import ObjectId

# Defining the Blueprint for tasks to organize routes in a separate file
tasks_bp = Blueprint("tasks", __name__)

@tasks_bp.route("/tasks", methods=["GET"])
def get_tasks():
    """Fetches all tasks from the 'todo' collection"""
    col = get_collection("todo")
    # Retrieve all documents from the collection and convert cursor to list
    db_tasks = list(col.find())
    
    for task in db_tasks:
        # MongoDB uses ObjectId which is not JSON serializable, so we convert it to string
        task["_id"] = str(task["_id"])
        
    return jsonify({"success": True, "data": db_tasks})

@tasks_bp.route("/tasks", methods=["POST"])
def create_task():
    """Creates a new task and ensures naming consistency for sub-tasks"""
    data = request.get_json(silent=True)
    
    new_task = {
        "title": data.get("title", "Untitled").strip(),
        "body": data.get("body", "").strip(),
        "priority": int(data.get("priority", 1)),
        "completed": False,
        # Using 'sub_tasks' consistently across the app
        "sub_tasks": data.get("sub_tasks") or data.get("subtasks") or []
    }
    
    col = get_collection("todo")
    col.insert_one(new_task)
    new_task["_id"] = str(new_task["_id"])
    return jsonify({"success": True, "data": new_task}), 201

@tasks_bp.route("/tasks/<task_id>", methods=["PUT"])
def update_task(task_id):
    """Updates specific fields of a task using the $set operator"""
    data = request.get_json(silent=True)
    col = get_collection("todo")
    
    # Use ObjectId to find the specific document and $set to update only provided fields
    col.update_one({"_id": ObjectId(task_id)}, {"$set": data})
    
    return jsonify({"success": True})

@tasks_bp.route("/tasks/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    """Deletes a task document by its ID"""
    col = get_collection("todo")
    # Perform the deletion based on the unique ObjectId
    col.delete_one({"_id": ObjectId(task_id)})
    
    return jsonify({"success": True})

@tasks_bp.route("/tasks/<task_id>", methods=["GET"])
def get_single_task(task_id):
    """Fetches a single task by its ID for detailed view"""
    col = get_collection("todo")
    # Find one document that matches the given ID
    task = col.find_one({"_id": ObjectId(task_id)})
    
    if task:
        task["_id"] = str(task["_id"])
        
    return jsonify({"success": True, "data": task})