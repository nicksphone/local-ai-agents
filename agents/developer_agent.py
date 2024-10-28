import os
import sys
from utils import generate_response

os.environ["PYTHONIOENCODING"] = "utf-8"
sys.stdout.reconfigure(encoding='utf-8')

class DeveloperAgent:
  def __init__(self):
      self.current_task = None
      self.code_output = ""
      self.documentation = ""

  def receive_task(self, task, specifications=None):
      """
      Receives a task and its specifications
      """
      self.current_task = task
      if specifications:
          prompt = f"Implement this task with these specifications:\nTask: {task}\nSpecs: {specifications}"
      else:
          prompt = f"Implement this task:\n{task}"
          
      self.code_output = generate_response(prompt)
      return self.code_output

  def create_documentation(self):
      """
      Creates documentation for the implemented code
      """
      if not self.code_output:
          return "No code to document"
          
      prompt = f"Create documentation for this code:\n{self.code_output}"
      self.documentation = generate_response(prompt)
      return self.documentation

  def get_code_output(self):
      """
      Returns the current code output
      """
      return self.code_output

  def get_documentation(self):
      """
      Returns the current documentation
      """
      return self.documentation

  def review_code(self):
      """
      Reviews the current code output
      """
      if not self.code_output:
          return "No code to review"
          
      prompt = f"Review this code and provide feedback:\n{self.code_output}"
      review_feedback = generate_response(prompt)
      return review_feedback