from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    response = {"message": "This service returns a 404 status code"}
    return jsonify(response), 404  # Возвращает статус-код 404
