import requests
import json

def list_models():
    try:
        # Ollama server URL
        server_url = "http://192.168.8.5:11434"

        # Endpoint to list available models
        list_endpoint = f"{server_url}"

        # Headers
        headers = {
            "Content-Type": "application/json"
        }

        # Send GET request to the list models endpoint
        response = requests.get(list_endpoint, headers=headers)

        # Raise an exception for HTTP error codes
        response.raise_for_status()

        # Parse the JSON response
        models = response.json()

        # Print the list of models
        print("Available Models:")
        for model in models.get('models', []):
            print(f"- {model}")

    except requests.exceptions.RequestException as e:
        print(f"Error listing models: {e}")

if __name__ == "__main__":
    list_models()
