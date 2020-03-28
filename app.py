from flask import Flask, jsonify, request, abort, Response
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'hello world!!'

@app.route('/greetings')
def return_greetings():
    hello = ["hello", "hey", "whatup"]
    return jsonify(greetings=hello)    

blabs = [1, 2, 3, 4, 5]

@app.route('/blabs', methods=['GET'])
def get_blabs():
    newArray = []
    args = request.args
    initial_time = args.get("createdSince")
    for blab in blabs:
        if (blab.get("postTime") >= int(initial_time)):
            newArray.append(blab)
    return jsonify(newArray)

@app.route('/blabs', methods=['POST'])
def add_blabs():
    return 0
    
@app.route('/blabs/<id>', methods=['DELETE'])
def remove_blabs(id):
    for blab in blabs:
        if blab["id"] == id:
            blabs.remove(blab)
        return Response(blab, status=200, mimetype='application/json')
    return abort(404)


#{
#
#    "id": "string",
#    "postTime": 0,
#    "author": 
#
#    {
#        "email": "user@example.com",
#        "name": "string"
#    },
#    "message": "string"
#
#}

#structure[key]

app.run()

