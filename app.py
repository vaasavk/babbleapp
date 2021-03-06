from flask import Flask, jsonify, request, abort, Response, make_response
import pymongo as database
import time
from dotenv import load_dotenv
from prometheus_flask_exporter import PrometheusMetrics
from prometheus_client import Counter
import os

app = Flask(__name__)

path = os.getenv('EnvVarPath')

load_dotenv(dotenv_path=path)
mongoHost = os.getenv('DATABASE_HOST', 'mongo')
mongoPort = os.getenv('DATABASE_PORT', '27017')

metrics = PrometheusMetrics(app)
totalBlabsCreated = Counter("AllBlabsCounter", "The total amount of blabs that have ever been created")
totalBlabsRemoved = Counter("BlabsRemoved", "The total amount of blabs that have been deleted")
totalBlabsGotten = Counter("BlabsGotten", "The total number of times get blabs has been called")
mongoClient = database.MongoClient("mongodb://%s:%s" % (mongoHost, mongoPort))
mongoBabbles = mongoClient["babble"]["blabs"]

blabs = []
blabId = 0

@app.route('/api/blabs', methods=['GET'])
def get_blabs():
    totalBlabsGotten.inc()
    newArray = []
    args = request.args
    initial_time = args.get("createdSince")
    if initial_time is None:
        initial_time = 0
    for blab in mongoBabbles.find():
        if (blab.get("postTime") >= int(initial_time)):
            temp = blab.copy()
            temp['id'] = str(blab['_id'])
            del temp['_id']
            newArray.append(temp)
    return make_response(jsonify(newArray), 200)

@app.route('/api/blabs', methods=['POST'])
def add_blabs():
    totalBlabsCreated.inc()
    global blabId
    thisAuthor = request.get_json().get('author')
    thisMessage = request.get_json().get('message')
    thisBlab = {
        'postTime': int(time.time()),
        'author': thisAuthor,
        'message': thisMessage
    }
    mongoBabbles.insert_one(thisBlab)
    blabId += 1
    localId = str(thisBlab['_id'])
    del thisBlab['_id']
    thisBlab['id'] = localId
    return make_response(jsonify(thisBlab), 201)
    
@app.route('/api/blabs/<id>', methods=['DELETE'])
def remove_blabs(id):
    idToRemove = {'_id': int(id)}
    blabToDelete = mongoBabbles.find_one(idToRemove)
    if blabToDelete:
        toDelete = blabToDelete.copy()
        mongoBabbles.delete_one(blabToDelete)
        totalBlabsRemoved.inc()
        return make_response(jsonify(toDelete), 200)
    return abort(404)
    