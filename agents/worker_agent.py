import os
from threading import Thread
from utils import generate_response

class WorkerAgent(Thread):
    def __init__(self, worker_id, structured_task, output_format, output_directory, callback):
        super().__init__()
        self.worker_id = worker_id
        self.structured_task = structured_task
        self.output_format = output_format
        self.output_directory = output_directory
        self.callback = callback

    def run(self):
        """
        Execute the assigned task and invoke the callback with the result.
        """
        work = self.execute_task()
        self.callback(self.worker_id, work)

    def execute_task(self):
        """
        Generates a response for the assigned task using the LLM.
        """
        if self.output_format == "code":
            # Generate code based on the structured task
            prompt = f"Write complete code for the following task:\n{self.structured_task['task']}"
            code_output = generate_response(prompt)

            # Return the structured task with generated code
            return {"task": self.structured_task['task'], "files": self.structured_task['files']}
        elif self.output_format == "text":
            # Handle text output
            prompt = f"Write a detailed response for the following task:\n{self.structured_task['task']}"
            text_output = generate_response(prompt)

            return {"task": self.structured_task['task'], "files": {"output.txt": text_output}}
        elif self.output_format == "image":
            # Handle image generation
            prompt = f"Create an image for the following task:\n{self.structured_task['task']}"
            image_output = generate_response(prompt)  # Assuming this returns image data

            return {"task": self.structured_task['task'], "files": {"output.png": image_output}}
        else:
            return {"task": self.structured_task['task'], "files": {}}