from flask import Flask, escape, request

app = Flask(__name__)

@app.route('/')
def hello():
    # get param from http://127.0.0.1:5000/?name=value
    name = request.args.get("name", "World")
    return f'Hello, {escape(name)}!'
