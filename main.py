from flask import Flask, render_template, request, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = ""
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

class Todo(db.Model):
     id = db.Column(db.Integer, primary_key=True)
     title = db.Column(db.String(100))
     complete = db.Column(db.Boolean)

@app.route("/")
def home():
    return render_template("home.html")


if __name__ == "__main__":
     db.create_all()
     app.run(debug=True)
