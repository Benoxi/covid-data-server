import flask
from flask import request, jsonify
from flask_cors import CORS, cross_origin
import requests
import schedule
from tinydb import TinyDB, Query
import json

app = flask.Flask(__name__)
cleanDb = True;

CORS(app, resources = {
        r'/api/*': {    
            "origins":
            [
                "http://localhost:8080",
                "https://localhost:8080",
                "http://covid-data-client.herokuapp.com",
                "https://covid-data-client.herokuapp.com"
            ]
        }
    }
)

# Initializing database:
db = TinyDB('database/db.json')

global covidData, countryData

# DOINE: Add simple API call that gets, fresh data!

#? TODO: Add database
#! TODO: Add countries - requests.get("https://restcountries.eu/rest/v2/all")
#! TODO: Format countries

def dumbIndexJsonObjects(data):
    # Alphabetically sort the data
    data.sort(key=lambda x: x['country'])
    # Index all the data
    i = 0
    for d in data:
        d['id'] = i
        i += 1

    return data

def resetDatabase(newData):
    db.purge()
    db.insert_multiple(newData)

def quickDbUpdate(newData):
    dbData = db.all() # Get all db data
    resetDb = False

    if len(newData) != len(dbData):
        # Some new data must be added or split, clean database!
        resetDatabase(newData)
    else:
        # Iterate through all docs and update
        i = 0
        for data in dbData:
            if  data['country'] == newData[i]['country']:
                data.update(newData[i])
            else:
                # Something must be different in the DB (1 item got removed and new one added)
                resetDb = True
                break
            i += 1

        if resetDb == True:
            resetDatabase(newData)
        else:
            db.write_back(dbData)

def queryForData():
    covidData = requests.get("https://coronavirus-19-api.herokuapp.com/countries")
    covidDataObjects = json.loads(covidData.text)
    covidDataObjects = dumbIndexJsonObjects(covidDataObjects)
    with app.app_context():
        if len(db) > 0:
            quickDbUpdate(covidDataObjects)
        else:
            db.insert_multiple(covidDataObjects)

schedule.every(10).minutes.do(queryForData)

# Update after server deployment
queryForData()

@app.route('/api/v1/covid', methods=['GET'])
def covidDataRequest():
    return jsonify(db.all())

# A welcome message to test our server
@app.route('/')
def index():
    return "<h2>Welcome to our server. If you see this then the server should be up!</h2>"

if __name__ == '__main__':
    app.run(threaded=True, port=5000)

