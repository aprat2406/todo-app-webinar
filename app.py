import os
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Database config (works for Heroku + DigitalOcean)
database_url = os.getenv("DATABASE_URL", "sqlite:///todo.db")

# Fix for Heroku postgres URL (postgres:// → postgresql://)
if database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql://", 1)

app.config["SQLALCHEMY_DATABASE_URI"] = database_url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# Model
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)

# Create DB
@app.before_first_request
def create_tables():
    db.create_all()

# Routes
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        content = request.form.get("content")
        if content:
            new_task = Todo(content=content)
            db.session.add(new_task)
            db.session.commit()
        return redirect("/")

    todos = Todo.query.all()
    return render_template("index.html", todos=todos)

@app.route("/delete/<int:id>")
def delete(id):
    task = Todo.query.get(id)
    if task:
        db.session.delete(task)
        db.session.commit()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
