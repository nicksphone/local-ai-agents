import os
import uuid
import threading
from datetime import datetime
from agents.worker_agent import WorkerAgent
from utils import generate_response

class CEOAgent:
    def __init__(self):
        self.tasks = []
        self.workers = {}
        self.completed_works = []  # Store completed works
        self.output_directory = ""  # Directory for output files
        self.assembled_work = ""  # Initialize assembled_work to an empty string
        self.outputs = []  # Initialize outputs to an empty list

    def process_input(self, user_input):
        """
        Break down the user's input into individual tasks using the LLM.
        """
        prompt = f"Create a clear and concise plan for {user_input}. Include the necessary code files and their structure."
        tasks = generate_response(prompt).split('\n')
        self.tasks = [task.strip() for task in tasks if task.strip()]

    def dispatch_workers(self):
        """
        Create and start Worker Agents for each approved task.
        """
        # Create a unique directory for this input question
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.output_directory = os.path.join(os.getcwd(), f"output_{timestamp}")
        os.makedirs(self.output_directory, exist_ok=True)

        threads = []
        for task in self.tasks:
            worker_id = str(uuid.uuid4())
            output_format = self.determine_output_format(task)
            structured_task = self.structure_task(task, output_format)
            worker = WorkerAgent(worker_id, structured_task, output_format, self.output_directory, callback=self.receive_work)
            self.workers[worker_id] = worker
            thread = threading.Thread(target=worker.run)
            threads.append(thread)
            thread.start()

        # Wait for all workers to complete
        for thread in threads:
            thread.join()

        # After all tasks are completed, provide explanations
        self.provide_explanations()

    def determine_output_format(self, task):
        """
        Determine the expected output format based on the task description.
        """
        if "program" in task or "code" in task:
            return "code"
        elif "image" in task:
            return "image"
        elif "write" in task or "story" in task or "text" in task:
            return "text"
        else:
            return "text"  # Default to text if not specified

    def structure_task(self, task, output_format):
        """
        Structure the task based on the output format.
        """
        if output_format == "code":
            # Example: Create a file tree structure for programming tasks
            file_structure = {
                "main.py": "# Main file for the application\n\nif __name__ == '__main__':\n    pass",
                # Add more files as needed
            }
            return {"task": task, "files": file_structure}
        elif output_format == "text":
            return {"task": task, "files": {"output.txt": "Generated text content."}}
        elif output_format == "image":
            return {"task": task, "files": {"output.png": "Image data or path."}}
        else:
            return {"task": task, "files": {}}

    def receive_work(self, worker_id, work):
        """
        Receive completed work from a Worker Agent.
        """
        self.workers.pop(worker_id)
        self.completed_works.append(work)
        self.outputs.append(work)  # Collect outputs for display

    def provide_explanations(self):
        """
        Provide explanations for the actions taken during the task processing.
        """
        # Output the files to the created directory
        for work in self.completed_works:
            for filename, content in work['files'].items():
                file_path = os.path.join(self.output_directory, filename)
                with open(file_path, "w") as file:
                    file.write(content)

        # Assemble the final output
        self.assembled_work = "\n".join([f"{work['task']} - Output files: {', '.join(work['files'].keys())}" for work in self.completed_works])
