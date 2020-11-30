from flask import Flask, escape, request
import joblib

app = Flask(__name__)

@app.route('/')
def hello():
    # get param from http://127.0.0.1:5000/?name=value
    name = request.args.get("name", "World")
    return f'Hello, {escape(name)}!'

@app.route('/predict_price')
def day_head():
    test = joblib.load('../test_testset.joblib')

    model = joblib.load('../test_model.joblib')
    pred = model.predict(test)[0]

    return {'test_values': test, 'day-ahead prediction': pred}
