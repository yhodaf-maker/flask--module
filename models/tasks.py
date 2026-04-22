from bson import ObjectId

# This function formats a database document into a clean dictionary for the API response
def format_task(task):
    return {
        "_id": str(task["_id"]),
        "title": task["title"],
        "body": task.get("body", ""),
        "completed": task.get("completed", False),
        "priority": task.get("priority", 1)  # Default to 1 (Low) if not exists
    }

# This function defines the initial structure of a new task
def create_task_model(title, body="", priority=1):
    return {
        "title": title.strip(),
        "body": body.strip(),
        "priority": priority,
        "completed": False
    }