from flask import Flask, request
from witTest import wit_response, pass_city_data, get_weather_data, determine_response
from pymessenger import Bot
import os, sys
import json
import requests

app = Flask(__name__)

bot = Bot

PAGE_ACCESS_TOKEN = 'EAACS1Eu5V2YBAJZCsZCPnJhv391Hm0nzQjdYMI99M73QDmrIOKdYpFYxlTANd0k5HTs8s5utqGduVOAjk5hG4ktnS1L4fTitsF7ibmwsejEWzvdiVxlfyUogVAPC9YCphkFFJaiVTHTvscydRjQpZBnTma3Ctdn6ZCwbw1oLDwZDZD'

@app.route('/', methods=['GET'])
def verify():
    if request.args.get('hub.mode') == 'subscribe' and request.args.get('hub.challenge'):
        if not request.args.get('hub.verify_token') == 'hello':
            return 'Verification token mismatch', 403
        return request.args['hub.challenge'], 200
    return 'Hello World', 403

@app.route('/', methods=['POST'])
def webhook():
    data = request.get_json()
    if data["object"] == "page":
        for entry in data["entry"]:
            for messaging_event in entry["messaging"]:
                if messaging_event.get("message"):
                    sender_id = messaging_event["sender"]["id"]
                    recipient_id = messaging_event["recipient"]["id"]
                    message_text = messaging_event["message"]["text"]
                    send_message_response(sender_id, parse_natural_text(message_text))
    return "ok"

def parse_natural_text(message_text):
    return determine_response(message_text)

def send_message(sender_id, message_text):
    '''
    Sending response back to the user using facebook graph API
    '''
    r = requests.post("https://graph.facebook.com/v2.6/me/messages",

        params={"access_token": PAGE_ACCESS_TOKEN},

        headers={"Content-Type": "application/json"},

        data=json.dumps({
        "recipient": {"id": sender_id},
        "message": {"text": message_text}
    }))

def send_message_response(sender_id, message_text):
    sentenceDelimiter = ". "
    messages = message_text.split(sentenceDelimiter)

    for message in messages:
        send_message(sender_id, message)

def log(message):
    sys.stdout.flush()

if __name__ == '__main__':
    app.run(debug = True, port = 5000)
