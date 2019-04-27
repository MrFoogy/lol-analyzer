from flask import Flask
from flask_cors import CORS
from flask import json, jsonify
import requests
app = Flask(__name__)
CORS(app)

api_key = "RGAPI-432bb4a2-c320-4c6d-96be-b73634c56748"
region_end_points = {
    "br": "br1.api.riotgames.com",
    "eune": "eun1.api.riotgames.com",
    "euw": "euw1.api.riotgames.com",
    "jp": "jp1.api.riotgames.com",
    "kr": "kr.api.riotgames.com",
    "lan": "la1.api.riotgames.com",
    "las": "la2.api.riotgames.com",
    "na": "na1.api.riotgames.com",
    "oce": "oc1.api.riotgames.com",
    "tr": "tr1.api.riotgames.com",
    "ru": "ru.api.riotgames.com",
}


@app.route("/")
def hello():
    return "Hello World!"


@app.route("/api/<server>/<summoner_name>/overview")
def get_summoner_overview(server, summoner_name):
    url = compose_url("/lol/summoner/v4/summoners/by-name/" + summoner_name, server)
    json_data = requests.get(url).json()
    return jsonify({k: json_data[k] for k in ["name", "summonerLevel", "profileIconId"]})


@app.route("/api/<server>/<summoner_name>/accountId")
def get_summoner_account_id(server, summoner_name):
    url = compose_url("/lol/summoner/v4/summoners/by-name/" + summoner_name, server)
    json_data = requests.get(url).json()
    return json_data["accountId"]


def compose_url(url, server):
    return "https://" + region_end_points[server] + url + "?api_key=" + api_key

if __name__ == "__main__":
    app.run()
