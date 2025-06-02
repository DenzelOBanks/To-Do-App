from flask import Flask, render_template,request,url_for,redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "To-do"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class todo(db.Model):
     id = db.Column(db.Integer, primary_key=True)
     title = db.Column(db.String(100))
     complete = db.Column(db.Boolean)

@app.route("/")
def index():
    todo_list = todo.query.all()
    return render_template("base.html", todo_list=todo_list)

@app.route("/add", methods=["POST"])
def add():
    title = request.form.get("title")
    new_todo = todo(title=title, complete=False)
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for("index"))


if __name__ == "__main__":
     with app.app_context():
      db.create_all()
      app.run(debug=True)
