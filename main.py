from flask import Flask, request
from dotenv import load_dotenv, find_dotenv
import json
import os

from openai_functions import chat_complition
from twilio_functions import send_message

load_dotenv(find_dotenv())

app = Flask(__name__)

# File to store conversation memory
MEMORY_FILE = 'conversation_memory.json'

def load_memory():
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, 'r') as file:
            return json.load(file)
    return {}

def save_memory(memory):
    with open(MEMORY_FILE, 'w') as file:
        json.dump(memory, file)

def add_to_memory(sender_id, message, response):
    memory = load_memory()
    if sender_id not in memory:
        memory[sender_id] = []
    memory[sender_id].append({'message': message, 'response': response})
    save_memory(memory)

def get_conversation_context(sender_id):
    memory = load_memory()
    return memory.get(sender_id, [])

@app.route('/')
def home():
    return 'All is well...'

@app.route('/twilio/receiveMessage', methods=['POST'])
def receiveMessage():
    try:
        # Extract incoming parameters from Twilio
        message = request.form['Body']
        sender_id = request.form['From']

        # Retrieve past conversations for context
        context = get_conversation_context(sender_id)
        context_text = " ".join([f"User: {conv['message']} Bot: {conv['response']}" for conv in context])

        # Get response from OpenAI with context
        result = chat_complition(message, context=context_text)
        if result['status'] == 1:
            response = result['response']
            send_message(sender_id, response)
            add_to_memory(sender_id, message, response)
    except Exception as e:
        print(f"Error: {e}")
        pass
    return 'OK', 200

if __name__ == '__main__':
    app.run(debug=True)
