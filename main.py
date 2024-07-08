from flask import Flask, request
from dotenv import load_dotenv, find_dotenv

from openai_functions import chat_complition
from twilio_functions import send_message


load_dotenv(find_dotenv())


app = Flask(__name__)


@app.route('/')
def home():
    return 'All is well...'


@app.route('/twilio/receiveMessage', methods=['POST'])
def receiveMessage():
    try:
        # Extract incomng parameters from Twilio
        message = request.form['Body']
        sender_id = request.form['From']

        # Get response from Openai
        result = chat_complition(message)
        if result['status'] == 1:
            send_message(sender_id, result['response'])
    except:
        pass
    return 'OK', 200
