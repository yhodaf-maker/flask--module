from flask import Flask,  jsonify, request
from werkzeug.exceptions import BadRequest, NotFound, UnprocessableEntity
import uuid

app = Flask(__name__)


tasks = [
    {"id": 1, "title": "Learn Flask", "completed": False},
    {"id": 2, "title": "Build API", "completed": False},
    {"id": 3, "title": "Test with Postman", "completed": True}
]

#error handling
@app.errorhandler(BadRequest)
@app.errorhandler(NotFound)
@app.errorhandler(UnprocessableEntity)
def handle_http_exception(e):
    return jsonify({
        "success": False,
        "error": e.name,
        "message": e.description
    }), e.code

# get all tasks
@app.route('/tasks', methods=['GET'])
def get_tasks():
    return jsonify({
        "success": True,
        "tasks": tasks
    })

#get task by id
@app.route('/tasks/<task_id>', methods=['GET'])
def get_task(task_id):
    for task in tasks:
        if task["id"] == task_id:
            return jsonify({
                "success": True,
                "task": task
            })

    raise NotFound("Task not found")

#create a new task
@app.route('/tasks', methods=['POST'])
def create_task():
   
    body = request.json
    if body == {}:
       raise BadRequest("No JSON body provided")
   
    title = body.get("title")
    
    if not isinstance(title, str):
        raise BadRequest("Title must be a string")
    
    if not title.strip():
        raise UnprocessableEntity("Title cannot be empty")
    
    new_task = {
        "id": str(uuid.uuid4()),
        "title": body["title"],
        "completed": False
    }

    tasks.append(new_task)
    
    return jsonify({
        "success": True,
        "task": new_task
    }), 201

#task update
@app.route('/tasks/<task_id>', methods=['PUT'])
def update_task(task_id):
    body = request.json
    keys = body.keys()
    body_keys = ["title", "completed"]
    
    if not body:
        raise BadRequest("No JSON body provided")

    for key in keys:
        if key not in body_keys:
            raise BadRequest(f"not allowed to pass:: {key}")
        
    if task_id not in [task["id"] for task in tasks]:
        raise NotFound("Task not found")
    
    for task in tasks:
        if task["id"] == task_id:

            
            if "title" in body:
                task["title"] = body["title"]
                

            
            if "completed" in body:
                task["completed"] = body["completed"]

            return jsonify({
                "success": True,
                "task": task
            }), 200
    
        raise NotFound("Task not found")

#task delete
@app.route('/tasks/<task_id>', methods=['DELETE'])
def delete_task(task_id):

    for task in tasks:
        if task["id"] == task_id:
            tasks.remove(task)

            return jsonify({
                "success": True,
                "message": "Task deleted"
            }), 200

    raise NotFound("Task not found")
    
       
if __name__ == '__main__':
    app.run(debug=True)