from flask import Flask
import platform

app = Flask(__name__)

@app.route("/")
def home():
    return "Hello, this is a simple API!"

@app.route('/version', methods=['GET'])
def get_version():
    # Получаем информацию о версии системы
    system_version = {
        "system": platform.system(),
        "version": platform.version(),
        "release": platform.release()
    }
    return system_version