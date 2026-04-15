from asyncio import tasks

from flask import Flask, jsonify, request
from datetime import datetime  , timezone 



app = Flask(__name__)

@app.route("/")
def home():
    return jsonify({
        "message": "API is running"
        })
    
@app.route("/status")
def status():
    return jsonify({
        "status": "OK",
        "version": "1.0.0"
        })   
     
@app.route("/time")
def time():
    now = datetime.now(timezone.utc).isoformat()
    return jsonify({
        "current_time": now
        })
    
@app.route("/info")   
def info():
    return jsonify({
        "app": "My First Flask App",
        "author": "student",
        "day": 2
        })
@app.route("/echo", methods=["POST"])
def echo():
    body = request.json
    
    if not bool(body):
        return jsonify({"success": False,
                        "message": "No JSON body provided"
                        }), 400
        
    return jsonify({"success": True,
                        "echo": body}), 200    
    

USERS = [
    {"id": 1, "name": "Alice"}, 
    {"id": 2, "name": "Bob"}, 
    {"id": 3, "name": "Charlie"}        
]

@app.route("/search")
def search():
    name = request.args.get("name")
    
    if not name:
        return 
    
@app.route('/tasks/<int:task_id>/', methods=['PUT'])
@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    body = request.json

    
    if not body:
        return jsonify({
            "success": False,
            "message": "No JSON body provided"
        }), 400

    
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

    return jsonify({
        "success": False,
        "message": "Task not found"
    }), 404

if __name__ == "__main__":
    app.run(debug=True)

