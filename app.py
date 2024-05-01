from flask import Flask, request, jsonify
from flask_cors import CORS
from promptHandler import handlePrompt
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.

app = Flask(__name__)
CORS(app)

@app.route('/')
def hello_world():
    return 'Hello, World! Lets get it done'

@app.route('/process_prompt', methods=['POST'])
def process_prompt():
    if request.is_json:
        # Extract the prompt from the received JSON data
        data = request.get_json()
        prompt = data.get('prompt', None)

        if prompt:

            # Process the prompt as needed
            print(prompt)
            return jsonify({'message': 'Received prompt successfully!', 'yourPrompt': prompt, 'response': handlePrompt({"thread_id": "thread_il6HBtqqUx07Q8HNYpmNXKvv", "prompt": prompt, })}), 200
        else:
            return jsonify({'error': 'No prompt provided'}), 400
    else:
        return jsonify({'error': 'Request must be JSON'}), 400

if __name__ == '__main__':
    app.run(debug=True)


