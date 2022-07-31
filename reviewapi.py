#GameShare reviews API
#Andrew James

from flask import Flask, request
import firebase_admin
import json
from firebase_admin import credentials
from firebase_admin import firestore
from flask_cors import CORS

# Use the application default credentials
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

app = Flask(__name__)
CORS(app)

#display all reviews in db
@app.route('/reviews', methods=['GET'])
def allreviews():
    reviews = db.collection('reviews').get()
    revlist = []
    for review in reviews:
        revlist.append(review.to_dict())
    return json.dumps(revlist)

#get review by game id
@app.route('/reviews/<gameid>', methods=['GET'])
def review(gameid):
    reviews = db.collection('reviews').where("id", "==", gameid).get()
    review = reviews[0].to_dict()
    return json.dumps(review)

#delete review by using it's game id
@app.route('/reviews/delete/<gameid>', methods=['GET', 'DELETE'])
def deletegame(gameid):
    reviews = db.collection('reviews').where("id", "==", gameid).get()
    docid = reviews[0].id
    db.collection('reviews').document(docid).delete()
    return '',204

#get review stars only using game id
@app.route('/reviews/stars/<gameid>', methods=['GET'])
def totalstars(gameid):
    reviews  = db.collection('reviews').where("id", "==", gameid).get()
    revlist = []
    for review in reviews:
        revlist.append(review.to_dict())
    return json.dumps(revlist[0]['totalStars'])

#get review text by game id
@app.route('/reviews/text/<gameid>', methods=['GET'])
def text(gameid):
    reviews  = db.collection('reviews').where("id", "==", gameid).get()
    revlist = []
    for review in reviews:
        revlist.append(review.to_dict())
    return json.dumps(revlist[0]['text'])

#get review date only
@app.route('/reviews/date/<gameid>', methods=['GET'])
def date(gameid):
    reviews  = db.collection('reviews').where("id", "==", gameid).get()
    revlist = []
    for review in reviews:
        revlist.append(review.to_dict())
    return json.dumps(revlist[0]['date'])

#update review by gameID
@app.route('/reviews/update/<gameid>', methods=['PATCH'])
def update(gameid):
    request_data = request.get_json()
    reviews = db.collection('reviews').where("gameID", "==", gameid).get()
    docid = reviews[0].id
    totalStars = "None"
    text = "None"
    date = "None"
    data = {}

    if 'totalStars' in request_data:
        totalStars = request_data['totalStars']
        data['totalStars'] = totalStars

    if 'text' in request_data:
        text = request_data['text']
        data['text'] = text

    if 'date' in request_data:
        date = request_data['date']
        data['date'] = date

    data = {"totalStars" : totalStars, "date" : date, "text" : text}
    db.collection('reviews').document(docid).update(data)
    
    return '',200

#create new review
@app.route('/reviews/create', methods=['POST'])
def create():
    request_data = request.get_json()
    totalStars = "None"
    text = "None"
    date = "None"
    id = "None"
    data = {}

    if 'totalStars' in request_data:
        totalStars = request_data['totalStars']
        data['totalStars'] = totalStars

    if 'text' in request_data:
        text = request_data['text']
        data['text'] = text

    if 'date' in request_data:
        date = request_data['date']
        data['date'] = date

    if 'id' in request_data:
        id = request_data['id']
        data['id'] = id
    
    data = {"totalStars" : totalStars, "date" : date, "text" : text, "id" : id}
    db.collection('reviews').add(data)
    
    return '',201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3007)
