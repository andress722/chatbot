from flask import Flask, request
import requests
import os

app = Flask(__name__)

VERIFY_TOKEN = "meutoken123"
PAGE_ACCESS_TOKEN = os.environ.get("PAGE_ACCESS_TOKEN")  # ou coloque direto entre aspas

@app.route('/')
def index():
    return 'Servidor Flask rodando no Render!'

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    if request.method == 'GET':
        token = request.args.get('hub.verify_token')
        challenge = request.args.get('hub.challenge')
        if token == VERIFY_TOKEN:
            return str(challenge), 200
        return 'Token inválido', 403

    elif request.method == 'POST':
        data = request.get_json()
        for entry in data.get('entry', []):
            for messaging_event in entry.get('messaging', []):
                if 'message' in messaging_event:
                    sender_id = messaging_event['sender']['id']
                    message_text = messaging_event['message'].get('text')
                    if message_text:
                        resposta = f"Você disse: {message_text}"
                        send_message(sender_id, resposta)
        return "ok", 200

def send_message(recipient_id, message_text):
    url = "https://graph.facebook.com/v18.0/me/messages"
    params = {"access_token": PAGE_ACCESS_TOKEN}
    headers = {"Content-Type": "application/json"}
    payload = {
        "recipient": {"id": recipient_id},
        "message": {"text": message_text}
    }

    r = requests.post(url, params=params, headers=headers, json=payload)
    print("Resposta do envio:", r.status_code, r.text)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
