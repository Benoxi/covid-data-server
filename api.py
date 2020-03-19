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

# A welcome message to test our server
@app.route('/')
def index():
    return "<h2>Welcome to our server. If you see this the server is probably up!</h2>"

if __name__ == '__main__':
    app.run(threaded=True, port=5000)
