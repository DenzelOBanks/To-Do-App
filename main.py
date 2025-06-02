from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Set secret key for session management (should be set to a secure value)
app.secret_key = ""  # Make our own key

# Configure SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize SQLAlchemy with Flask app
db = SQLAlchemy(app)

# Define Todo model for the database
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Unique ID for each todo
    title = db.Column(db.String(100))             # Title of the todo item
    complete = db.Column(db.Boolean)              # Completion status

# Home route: display all todo items
@app.route("/")
def index():
    todo_list = Todo.query.all()  # Get all todo items from the database
    return render_template("base.html", todo_list=todo_list)  # Render template with todo list

# Add route: handle adding a new todo item
@app.route("/add", methods=["POST"])
def add():
    title = request.form.get("title")  # Get title from form submission
    new_todo = Todo(title=title, complete=False)  # Create new Todo object
    db.session.add(new_todo)  # Add to database session
    db.session.commit()       # Commit changes to database
    return redirect(url_for("index"))  # Redirect to home page

# Update route: toggle completion status of a todo item
@app.route("/update/<int:todo_id>")
def update(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()  # Find todo by ID
    todo.complete = not todo.complete                # Toggle complete status
    db.session.commit()                              # Commit changes
    return redirect(url_for("index"))                # Redirect to home page

# Delete route: remove a todo item
@app.route("/delete/<int:todo_id>")
def delete(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()  # Find todo by ID
    db.session.delete(todo)                          # Delete from database
    db.session.commit()                              # Commit changes
    return redirect(url_for("index"))                # Redirect to home page

# Run the app
if __name__ == "__main__":
    with app.app_context():
        db.create_all()      # Create database tables if they don't exist
        app.run(debug=True)  # Start Flask app in debug mode
