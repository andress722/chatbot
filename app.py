from flask import Flask, request
import os
import requests

app = Flask(__name__)
VERIFY_TOKEN = "meutoken123"
PAGE_ACCESS_TOKEN = os.environ.get("PAGE_ACCESS_TOKEN")

@app.route('/', methods=['GET'])
def index():
    return 'Bot online'

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    if request.method == 'GET':
        token = request.args.get('hub.verify_token')
        challenge = request.args.get('hub.challenge')
        if token == VERIFY_TOKEN:
            return str(challenge), 200
        return 'Token inválido', 403

    if request.method == 'POST':
        data = request.get_json()
        print(data)  # ADICIONE ISSO PRA VER OS POSTS!
        for entry in data.get('entry', []):
            for messaging_event in entry.get('messaging', []):
                sender_id = messaging_event['sender']['id']
                if 'message' in messaging_event:
                    text = messaging_event['message'].get('text')
                    send_message(sender_id, f"Você disse: {text}")
        return "ok", 200

def send_message(recipient_id, message):
    payload = {
        'recipient': {'id': recipient_id},
        'message': {'text': message}
    }
    auth = {'access_token': PAGE_ACCESS_TOKEN}
    requests.post('https://graph.facebook.com/v18.0/me/messages',
                  params=auth, json=payload)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
