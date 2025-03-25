from flask import Flask, request

app = Flask(__name__)

VERIFY_TOKEN = "meutoken123"

@app.route('/')
def index():
    return 'Servidor Flask rodando no Render!'

@app.route('/webhook', methods=['GET'])
def webhook():
    token = request.args.get('hub.verify_token')
    challenge = request.args.get('hub.challenge')

    if token == VERIFY_TOKEN:
        return str(challenge), 200
    return 'Token inválido', 403

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
