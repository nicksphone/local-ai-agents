import os
import sys
from utils import generate_response

os.environ["PYTHONIOENCODING"] = "utf-8"
sys.stdout.reconfigure(encoding='utf-8')

class ProductManagerAgent:
  def __init__(self):
      self.requirements = []
      self.specifications = []

  def analyze_task(self, task):
      """
      Analyzes the task and creates detailed requirements
      """
      prompt = f"As a Product Manager, create detailed requirements for this task:\n{task}"
      response = generate_response(prompt)
      self.requirements = [req.strip() for req in response.split('\n') if req.strip()]
      return self.requirements

  def create_specifications(self):
      """
      Creates technical specifications based on requirements
      """
      if not self.requirements:
          return []
      
      prompt = f"Create technical specifications for these requirements:\n{self.requirements}"
      response = generate_response(prompt)
      self.specifications = [spec.strip() for spec in response.split('\n') if spec.strip()]
      return self.specifications

  def get_requirements(self):
      """
      Returns the current requirements
      """
      return self.requirements

  def get_specifications(self):
      """
      Returns the current specifications
      """
      return self.specifications