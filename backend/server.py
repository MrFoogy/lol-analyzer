import sys
from flask import Flask
from flask_cors import CORS
from flask import json, jsonify, request, Response
import requests
import champion_data
import queue_names
import timeline_analysis
import match_details
app = Flask(__name__)
CORS(app)

api_key = "RGAPI-7c1c8152-238d-4671-96da-0c4566b1f4ac"
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

def allow_cors(request):
    request.setHeader('Access-Control-Allow-Origin', '*')
    request.setHeader('Access-Control-Allow-Methods', 'GET')
    request.setHeader('Access-Control-Allow-Headers',
                   'x-prototype-version,x-requested-with')
    request.setHeader('Access-Control-Max-Age', 2520)
    request.setHeader('Content-type', 'application/json')

def get_error_response(status_code):
    message = "Error"
    if status_code == 429:
        message = "API Key maxed out"
    return Response(message, status=status_code)


def is_error(response):
    return response.status_code != 200


@app.route("/")
def hello():
    return "Hello World!"


@app.route("/api/<server>/summoner/<summoner_name>/overview")
def get_summoner_overview(server, summoner_name):
    url = compose_url("/lol/summoner/v4/summoners/by-name/" + summoner_name, server)
    response = requests.get(url)
    if is_error(response):
        return get_error_response(response.status_code)
    json_data = response.json()
    return jsonify({k: json_data[k] for k in ["name", "summonerLevel", "profileIconId"]})


@app.route("/api/<server>/summoner/<summoner_name>/account")
def get_summoner_account_id(server, summoner_name):
    url = compose_url("/lol/summoner/v4/summoners/by-name/" + summoner_name, server)
    response = requests.get(url)
    if is_error(response):
        return get_error_response(response.status_code)
    json_data = response.json()
    return jsonify({k: json_data[k] for k in ["accountId", "id"]})


@app.route("/api/<server>/account/<account_id>/matchlist")
def get_matches(server, account_id):
    url = compose_url("/lol/match/v4/matchlists/by-account/" + account_id, server)
    response = requests.get(url)
    if is_error(response):
        return get_error_response(response.status_code)
    json_data = response.json()
    return jsonify([{**{k: match_obj[k] for k in ["gameId", "lane", "role", "timestamp"]}, 
                     "championName": champion_data.get_champion_name(match_obj["champion"]),
                     "queue": queue_names.get_queue_name(match_obj["queue"])} for match_obj in json_data["matches"]])


@app.route("/api/<server>/summoner/<summoner_id>/champion/mastery")
def get_champion_mastery(server, summoner_id):
    url = compose_url("/lol/champion-mastery/v4/champion-masteries/by-summoner/" + summoner_id, server)
    response = requests.get(url)
    if is_error(response):
        return get_error_response(response.status_code)
    json_data = response.json()
    return jsonify([{**{k: champ_obj[k] for k in ["championId", "championLevel", "championPoints"]}, 
                     "championName": champion_data.get_champion_name(champ_obj["championId"])} for champ_obj in json_data[:25]])


@app.route("/api/<server>/match_timeline/<match_id>")
def get_match_timeline(server, match_id):
    url = compose_url("/lol/match/v4/timelines/by-match/" + match_id, server)
    response = requests.get(url)
    if is_error(response):
        return get_error_response(response.status_code)
    json_data = response.json()
    return jsonify(timeline_analysis.get_timeline_data(json_data, request.args.get("event"), int(request.args.get("pID"))))


def fetch_combined_timeline(server, account_id, match_ids, event_type):
    combined_timeline = []
    num_matches = 0
    for match_id in match_ids:
        print("Number " + str(num_matches), flush=True)
        details_response = get_match_details(server, match_id)
        if is_error(details_response): 
            return get_error_response(details_response.status_code)
        participant_id = match_details.get_participant_id(details_response.json, account_id)
        if participant_id is None:
            continue
        url = compose_url("/lol/match/v4/timelines/by-match/" + match_id, server)
        match_timeline_response = requests.get(url)
        if is_error(match_timeline_response):
            return get_error_response(match_timeline_response.status_code)
        match_events = timeline_analysis.get_timeline_data(match_timeline_response.json(), event_type, participant_id)
        combined_timeline.extend(match_events)
        num_matches += 1
    return jsonify({"matches": num_matches, "timeline": combined_timeline})


@app.route("/api/<server>/account/<account_id>/combined_timeline")
def get_combined_timeline(server, account_id):
    match_ids = [str(matchId) for matchId in json.loads(request.args.get("matchIDs"))]
    print(match_ids, flush=True)
    event_type = request.args.get("event")
    return fetch_combined_timeline(server, account_id, match_ids, event_type)


@app.route("/api/<server>/account/<account_id>/full_timeline")
def get_full_timeline(server, account_id):
    matches_response = get_matches(server, account_id)
    if is_error(matches_response):
        return get_error_response(matches_response.status_code)
    matches = matches_response.json
    event_type = request.args.get("event")

    match_ids = [str(match["gameId"]) for match in matches[:20]]
    return fetch_combined_timeline(server, account_id, match_ids, event_type)


@app.route("/api/<server>/match/<match_id>")
def get_match_details(server, match_id):
    url = compose_url("/lol/match/v4/matches/" + match_id, server)
    response = requests.get(url)
    if is_error(response):
        return get_error_response(response.status_code)
    json_data = response.json()
    return jsonify(match_details.get_relevant_details(json_data))


def compose_url(url, server):
    return "https://" + region_end_points[server] + url + "?api_key=" + api_key

if __name__ == "__main__":
    app.run()
