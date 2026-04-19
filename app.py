from flask import Flask, render_template

from db import init_db
from errors import errors_bp
from routes.tasks import tasks_bp

# Main Flask app instance for the todo API.
app = Flask(__name__)

init_db(app)
# Register the task routes and shared error handlers.
app.register_blueprint(tasks_bp)
app.register_blueprint(errors_bp)


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

if __name__ == "__main__":
    
    app.run(debug=True)