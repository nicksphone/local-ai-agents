from flask import Flask, render_template, request, redirect, url_for
from agents.ceo_agent import CEOAgent

app = Flask(__name__)
ceo_agent = CEOAgent()

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        user_input = request.form["user_input"]
        ceo_agent.process_input(user_input)
        return redirect(url_for("approve_tasks"))  # Redirect to task approval page
    return render_template("index.html")

@app.route("/approve_tasks", methods=["GET", "POST"])
def approve_tasks():
    if request.method == "POST":
        approved_tasks = []
        revisions = request.form.get("revisions", "")  # Get any revisions from the input box
        
        # Process each task for approval
        for task in ceo_agent.tasks:
            task_key = task.replace(" ", "_")  # Create a unique key for each task
            if request.form.get(f"{task_key}_approve") == "yes":
                approved_tasks.append(task)

        # Update the tasks in the CEOAgent
        ceo_agent.tasks = approved_tasks  # Only keep approved tasks
        ceo_agent.dispatch_workers()  # Dispatch workers for the approved tasks

        # Handle revisions if any
        if revisions:
            ceo_agent.explanations.append(f"Revisions requested: {revisions}")

        return redirect(url_for("results"))  # Redirect to results page

    # Display the tasks for approval
    tasks = ceo_agent.tasks
    return render_template("approve_tasks.html", tasks=tasks)

@app.route("/results")
def results():
    assembled_work = ceo_agent.assembled_work
    outputs = ceo_agent.outputs  # Get outputs for display
    explanations = ceo_agent.explanations  # Get explanations for display
    return render_template("results.html", assembled_work=assembled_work, outputs=outputs, explanations=explanations)

if __name__ == "__main__":
    app.run(debug=True)  # Ensure debug mode is enabled for easier troubleshooting
