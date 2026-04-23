from bson import ObjectId

# This function formats a database document into a clean dictionary for the API response
def format_task(task):
    return {
        "_id": str(task["_id"]),
        "title": task["title"],
        "body": task.get("body", ""),
        "completed": task.get("completed", False),
        "priority": task.get("priority", 1),
        "sub_tasks": task.get("sub_tasks", [])  
    }

# This function defines the initial structure of a new task
def create_task_model(title, body="", priority=1, sub_tasks=None):
    return {
        "title": title.strip(),
        "body": body.strip(),
        "priority": priority,
        "completed": False,
        "sub_tasks": sub_tasks or []  
    }