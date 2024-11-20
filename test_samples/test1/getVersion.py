from flask import Flask
import platform

app = Flask(__name__)

@app.route("/")
def home():
    return "Hello, this is a simple API!"

