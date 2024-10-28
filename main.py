from flask import Flask, render_template, request, redirect, url_for
from agents.ceo_agent import CEOAgent

app = Flask(__name__)
ceo_agent = CEOAgent()

@app.route("/", methods=["GET", "POST"])
def index():
  if request.method == "POST":
      user_input = request.form["user_input"]
      ceo_agent.process_input(user_input)
      return redirect(url_for("approve_tasks"))
  return render_template("index.html")

@app.route("/approve_tasks", methods=["GET", "POST"])
def approve_tasks():
  if request.method == "POST":
      approved_tasks = []
      revisions = request.form.get("revisions", "")
      print(f"Revisions: {revisions}")
      
      task_summary = []
      for task in ceo_agent.tasks:
          task_key = task.replace(" ", "_")
          if request.form.get(f"{task_key}_approve") == "yes":
              approved_tasks.append(task)
              task_summary.append(task)

      ceo_agent.tasks = approved_tasks
      ceo_agent.dispatch_workers()

      if revisions:
          ceo_agent.explanations.append(f"Revisions requested: {revisions}")

      print("Approved Tasks Summary:")
      for task in task_summary:
          print(f"- {task}")

      return redirect(url_for("results"))

  tasks = ceo_agent.tasks
  return render_template("approve_tasks.html", tasks=tasks)

@app.route("/results")
def results():
  assembled_work = ceo_agent.assembled_work
  outputs = ceo_agent.outputs
  explanations = ceo_agent.explanations
  return render_template("results.html", 
                       assembled_work=assembled_work, 
                       outputs=outputs, 
                       explanations=explanations)

if __name__ == "__main__":
  app.run(debug=True)