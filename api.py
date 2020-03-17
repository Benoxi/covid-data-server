import flask
from flask import request, jsonify
from flask_cors import CORS, cross_origin
import requests
import schedule

app = flask.Flask(__name__)

# app.config["DEBUG"] = True
# CORS(app, resources=r'/api/*')

CORS(app, resources = {
        r'/api/*': {
            "origins": 
            [
                "http://localhost:8080",
                "http://covid-data-client.herokuapp.com"
            ]
        }
    }
)


global covidData, countryData

# //? TODO: Add simple API call that gets, fresh data!

# //! TODO: Add database
# //! TODO: Add countries - requests.get("https://restcountries.eu/rest/v2/all")
# //! TODO: Format countries

def queryForData():
    covidData = requests.get("https://lab.isaaclin.cn/nCoV/api/area")

schedule.every(10).minutes.do(queryForData)

covidData = requests.get("https://lab.isaaclin.cn/nCoV/api/area")

@app.route('/api/v1/covid', methods=['GET'])
def covidDataRequest():
    return jsonify(covidData.text   );

app.run()
