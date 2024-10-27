import requests
import json

def generate_response(prompt):
    """
    Generates a response from the specified Ollama model based on the provided prompt.

    Args:
        prompt (str): The input prompt from the user.

    Returns:
        str: The generated response from the model.
    """
    try:
        # Ollama server URL
        server_url = "http://192.168.8.5:11434/api/generate"

        # Fixed model name
        model = "llama3.1:8b"

        # Payload with fixed model
        payload = {
            "model": model,
            "prompt": prompt
        }

        # Headers
        headers = {
            "Content-Type": "application/json"
        }

        # Debug: Print the request details
        print(f"Sending POST request to: {server_url}")
        print(f"Payload: {json.dumps(payload)}")

        # Send POST request to the Ollama server
        response = requests.post(server_url, headers=headers, data=json.dumps(payload))

        # Debug: Print the response status code
        print(f"Received response with status code: {response.status_code}")

        # Print the raw response content for debugging
        raw_response = response.text
        print(f"Raw response content: {raw_response}")

        # Split the raw response into individual JSON objects
        json_objects = raw_response.strip().split('\n')

        # Initialize a variable to hold the complete response
        complete_response = ""

        # Process each JSON object
        for json_object in json_objects:
            try:
                # Parse the JSON object
                result = json.loads(json_object)

                # Accumulate the response text
                complete_response += result.get("response", "")

                # Check if the response is complete
                if result.get("done"):
                    break  # Stop processing if done
            except json.JSONDecodeError as e:
                print(f"JSON decode error: {e}")
                continue  # Skip any malformed JSON objects

        # Debug: Print the complete response
        print(f"Complete Response: {complete_response.strip()}")

        return complete_response.strip() if complete_response else "No valid response received."

    except requests.exceptions.RequestException as e:
        # Print the error for debugging purposes
        print(f"Error generating response: {e}")
        return "An error occurred while generating the response."
