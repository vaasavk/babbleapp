from flask import Flask, jsonify
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'hello world!!'

@app.route('/greetings')
def return_greetings():
    hello = ["hello", "hey", "whatup"]
    return jsonify(greetings=hello)    

app.run()