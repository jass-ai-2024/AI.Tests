from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "Server is running on port 4000!"  # Сообщение указывает неправильный порт
