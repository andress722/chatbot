from flask import Flask, request
import requests
import os

app = Flask(__name__)

# Substitua pelo seu token da página do Facebook
PAGE_ACCESS_TOKEN = os.environ.get("PAGE_ACCESS_TOKEN", "COLOQUE_SEU_TOKEN_AQUI")
VERIFY_TOKEN = "meutoken123"

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
        if data.get("object") == "page":
            for entry in data.get("entry", []):
                for messaging_event in entry.get("messaging", []):
                    if messaging_event.get("message"):
                        sender_id = messaging_event["sender"]["id"]
                        message_text = messaging_event["message"].get("text")
                        if message_text:
                            resposta = f"Você disse: {message_text}"
                            send_message(sender_id, resposta)
        return "ok", 200

def send_message(recipient_id, text):
    url = "https://graph.facebook.com/v18.0/me/messages"
    headers = {"Content-Type": "application/json"}
    payload = {
        "recipient": {"id": recipient_id},
        "message": {"text": text},
        "messaging_type": "RESPONSE",
        "access_token": PAGE_ACCESS_TOKEN
    }
    response = requests.post(url, headers=headers, json=payload)
    print("Envio de mensagem:", response.status_code, response.text)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
