import requests
import json
import sys

if sys.stdout.encoding != 'utf-8':
  sys.stdout.reconfigure(encoding='utf-8')

def generate_response(prompt):
  """
  Generates a response from the specified Ollama model based on the provided prompt.
  """
  try:
      server_url = "http://192.168.8.5:11434/api/generate"
      model = "llama3.1:8b"
      
      payload = {
          "model": model,
          "prompt": prompt
      }
      
      headers = {
          "Content-Type": "application/json"
      }

      print(f"Sending request to Ollama: {prompt[:100]}...")
      
      response = requests.post(server_url, headers=headers, json=payload)
      response.raise_for_status()
      
      raw_response = response.text
      json_objects = raw_response.strip().split('\n')
      complete_response = ""

      for json_object in json_objects:
          try:
              result = json.loads(json_object)
              complete_response += result.get("response", "")
              if result.get("done"):
                  break
          except json.JSONDecodeError as e:
              print(f"JSON decode error: {e}")
              continue

      return complete_response.strip() if complete_response else "No valid response received."

  except requests.exceptions.RequestException as e:
      print(f"Error generating response: {e}")
      return f"Error generating response: {str(e)}"