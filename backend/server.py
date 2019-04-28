import sys
from flask import Flask
from flask_cors import CORS
from flask import json, jsonify
import requests
import champion_data
import queue_names
import timeline_analysis
app = Flask(__name__)
CORS(app)

api_key = "RGAPI-eb0e7bb1-3c9d-47e9-98c8-2fea5b60466c"
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


@app.route("/api/<server>/<summoner_name>/account")
def get_summoner_account_id(server, summoner_name):
    url = compose_url("/lol/summoner/v4/summoners/by-name/" + summoner_name, server)
    json_data = requests.get(url).json()
    print(json_data, sys.stdout)
    return jsonify({k: json_data[k] for k in ["accountId", "id"]})


@app.route("/api/<server>/<account_id>/matchlist")
def get_matches(server, account_id):
    url = compose_url("/lol/match/v4/matchlists/by-account/" + account_id, server)
    json_data = requests.get(url).json()
    return jsonify([{**{k: match_obj[k] for k in ["gameId", "lane", "role", "timestamp"]}, 
                     "championName": champion_data.get_champion_name(match_obj["champion"]),
                     "queue": queue_names.get_queue_name(match_obj["queue"])} for match_obj in json_data["matches"]])


@app.route("/api/<server>/<summoner_id>/champion/mastery")
def get_champion_mastery(server, summoner_id):
    url = compose_url("/lol/champion-mastery/v4/champion-masteries/by-summoner/" + summoner_id, server)
    json_data = requests.get(url).json()
    return jsonify([{**{k: champ_obj[k] for k in ["championId", "championLevel", "championPoints"]}, 
                     "championName": champion_data.get_champion_name(champ_obj["championId"])} for champ_obj in json_data[:25]])


@app.route("/api/<server>/match_timeline/<match_id>/kills")
def get_match_kills(server, match_id):
    url = compose_url("/lol/match/v4/timelines/by-match/" + match_id, server)
    json_data = requests.get(url).json()
    return jsonify(timeline_analysis.get_all_kills(json_data))


def compose_url(url, server):
    return "https://" + region_end_points[server] + url + "?api_key=" + api_key

if __name__ == "__main__":
    app.run()
