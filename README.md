Here are all the dependencies needed to run this code. Create a requirements.txt file with these dependencies:

txt

Copy Code
flask==3.0.0
requests==2.31.0
python-dotenv==1.0.0

Installation steps for a new user:

    Create a virtual environment (recommended):

bash

Copy Code
python -m venv venv

# Activate the virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

    Install the dependencies:

bash

Copy Code
pip install -r requirements.txt

    Project structure should look like this:

chat_agents/
├── requirements.txt
├── main.py
├── utils.py
├── agents/
│   ├── __init__.py
│   ├── ceo_agent.py
│   └── worker_agent.py
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── approve_tasks.html
│   └── results.html
└── static/
    ├── styles.css
    └── loading.css

    Additional requirements:

    Python 3.8 or higher
    Ollama server running locally at http://192.168.8.5:11434 (or update the URL in utils.py to match your Ollama server)
    The llama3.1:8b model installed in Ollama (can be installed using ollama pull llama3.1:8b)

    Environment setup:
