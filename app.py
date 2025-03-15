from flask import Flask, render_template,request, redirect, url_for
import json

app= Flask(__name__)
TASK_FILE="tasks.json"

def load_tasks():
    try:
        with open(TASK_FILE,"r") as file:
            return json.load(file)
    except(FileNotFoundError, json.JSONDecodeError):
        return []

def save_tasks(tasks):
    with open(TASK_FILE,"w") as file:
        json.dump(tasks,file,indent=4)

@app.route('/')
def index():
    tasks=load_tasks()
    return render_template('index.html', tasks=tasks,enumerate=enumerate)

@app.route("/add",methods=["POST"])
def add_task():
    task_name=request.form.get("task")
    tasks=load_tasks()
    if task_name:
        tasks.append({"task": task_name, "completed":False})
        save_tasks(tasks)
    return redirect(url_for("index"))

@app.route("/complete/<int:task_id>")
def complete_task(task_id):
    tasks = load_tasks()
    if 0 <= task_id < len(tasks):
        tasks[task_id]["completed"] = True
        save_tasks(tasks)
    return redirect(url_for("index"))

@app.route("/delete/<int:task_id>")
def delete_task(task_id):
    tasks = load_tasks()
    if 0 <= task_id < len(tasks):
        tasks.pop(task_id)
        save_tasks(tasks)
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)