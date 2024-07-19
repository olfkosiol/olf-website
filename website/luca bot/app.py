from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

# Antworten aus einer JSON-Datei laden
try:
    with open('responses.json', 'r', encoding='utf-8') as file:
        responses = json.load(file)
        print("responses.json geladen: ", responses)  # Debugging-Ausgabe
except Exception as e:
    print(f"Fehler beim Laden der JSON-Datei: {e}")
    responses = {}

# Funktion zum Generieren einer Bot-Antwort
def get_bot_response(message):
    for keyword in responses:
        if keyword in message.lower():
            return responses[keyword]
    return 'Es tut mir leid, das verstehe ich nicht. Können Sie das bitte anders formulieren?'

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('chat message')
def handle_message(msg):
    print(f"Nachricht erhalten: {msg}")  # Debugging-Ausgabe
    emit('chat message', msg, broadcast=True)
    bot_response = get_bot_response(msg)
    print(f"Bot-Antwort: {bot_response}")  # Debugging-Ausgabe
    emit('bot response', bot_response, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
