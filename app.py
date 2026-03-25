from flask import Flask, render_template, request, redirect

app = Flask(__name__)

# In-memory storage (resets on restart)
todos = []

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        content = request.form.get("content")
        if content:
            todos.append(content)
        return redirect("/")

    return render_template("index.html", todos=todos)

@app.route("/delete/<int:index>")
def delete(index):
    if 0 <= index < len(todos):
        todos.pop(index)
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
