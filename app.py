from flask import Flask, request, render_template
import google.generativeai as genai
import config

api_key = config.api_key
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-pro')
chat = model.start_chat(history=[])

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        message = request.form.get('message')
        chat.send_message(message)
        formatted_history = parse_chat_history(chat.history)
        return render_template('index.html', chat_history=formatted_history)
    return render_template('index.html')

def parse_chat_history(chat_history):
    parsed_history = []
    for chat in chat_history:
        chat = str(chat)
        role = chat[chat.index('role')+7:chat.rfind('\"')]
        text = chat[chat.index('text')+7:chat.rfind('}')-2]
        text = parse_text_to_html(text)
        parsed_history.append({'role': role, 'text': text})
    return parsed_history

def parse_text_to_html(text):
    text = text.replace('\\n', '\n')
    text = text.replace("\\'", "\'")
    return text

if __name__ == '__main__':
    app.run(debug=True, port=8080)