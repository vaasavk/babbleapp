from flask import Flask, jsonify, request, abort, Response
import pymongo as database
import time
app = Flask(__name__)

mongoClient = database.MongoClient("mongodb://mongo:27017")
mongoBabbles = mongoClient["babble"]["blabs"]

blabs = []
idNumber = 0

@app.route('/blabs', methods=['GET'])
def get_blabs():
    newArray = []
    args = request.args
    initial_time = args.get("createdSince")
    if initial_time is None:
        initial_time = 0
    for blab in mongoBabbles.find():
        if (blab.get("postTime") >= int(initial_time)):
            newArray.append(blab)
    return make_response(jsonify(newArray), 200)

@app.route('/blabs', methods=['POST'])
def add_blabs():
    thisAuthor = request.get_json().get('author')
    thisMessage = request.get_json().get('message')
    if (createdSince == None):
        timeCreated = 0
    thisBlab = {
        '_id': idNumber,
        'postTime': int(time.time()),
        'author': thisAuthor,
        'message': thisMessage
    }
    idNumber += 1
    mongoBabbles.insert_one(thisBlab)
    return make_response(jsonify(response), 201)
    
@app.route('/blabs/<id>', methods=['DELETE'])
def remove_blabs(id):
    idToRemove = {'_id': int(id)}
    blabToDelete = mongoBabbles.find_one(idToRemove)
    if blabToDelete:
        toDelete = blabToDelete.copy()
        mongoBabbles.delete_one(blabToDelete)
        return make_response(jsonify(toDelete), 200)
    return abort(404)
