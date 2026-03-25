from flask import Flask, render_template, request, redirect

app = Flask(__name__)

# Global in-memory list
todos = []

@app.route("/", methods=["GET", "POST"])
def index():
    global todos

    if request.method == "POST":
        content = request.form.get("content")

        if content and content.strip():
            todos.append(content.strip())

        return redirect("/")  # Refresh page after adding

    return render_template("index.html", todos=todos)


@app.route("/delete/<int:index>")
def delete(index):
    global todos

    if 0 <= index < len(todos):
        todos.pop(index)

    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
