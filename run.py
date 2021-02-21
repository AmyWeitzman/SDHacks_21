from flask import render_template, request, redirect, url_for
from app import app
import requests

from app.models.ModeOfTransportation import get_all_mode_of_trans
from app.models.Action import get_all_actions

# Trip to Carbon API: https://triptocarbon.com/documentation/api/footprint
BASE_URL = "https://api.triptocarbon.xyz/v1/footprint"

# get transportation options from database
def getTransports():
    return get_all_mode_of_trans()

# get action suggestions from database
def getActions():
    return get_all_actions()

# build API request string based on params
def buildRequestStr(params):
    requestStr = BASE_URL
    requestStr += "?"  # add query params
    for idx, (key, val) in enumerate(params.items()):
        requestStr += key + "=" + val 
        if((idx + 1) < len(params)):  # still more params to add
            requestStr += "&"
    return requestStr

# calculate carbon footprint based on specified params
def calcCarbonFootprint(distance, transMode):
    params = {
        'activity': distance,
        'activityType': 'miles',
        'mode': transMode,
        'country': 'usa'
    }
    url = buildRequestStr(params)
    res = requests.get(url)
    data = res.json()
    return data["carbonFootprint"]

# homepage with input form
@app.route('/')
def index():
    transports = getTransports()
    return render_template("index.html", len=len(transports), transports=transports)

# url for input form submission
@app.route('/calculate', methods=['POST'])
def calculate():
    distance= request.form.get("distance")
    transMode = request.form.get("transports-dropdown")
    return redirect(url_for('results', distance=distance, transMode=transMode))

# results page with carbon footprint and suggested activities to reduce it
@app.route('/results')
def results():
    distance = request.args["distance"]
    transMode = request.args["transMode"]
    carbonFootprint = calcCarbonFootprint(distance, transMode)
    actions = getActions()
    return render_template("results.html", carbonFootprint=carbonFootprint, len=len(actions), actions=actions)

if __name__ == '__main__':
    app.run()