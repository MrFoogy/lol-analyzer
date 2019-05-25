import sys
from sanic import Sanic, response
from sanic_cors import CORS
import champion_data
import queue_names
import timeline_analysis
import match_details
import json
import certifi
import os
import asyncio
import aiohttp
#CORS(app)

app = Sanic()
CORS(app)

os.environ["SSL_CERT_FILE"] = certifi.where()

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

async def get_http_response(app, url):
    async with aiohttp.ClientSession() as session:
        return await session.get(url)


async def get_response_json(app, response):
    return await response.json()


def allow_cors(request):
    return

def get_error_response(status_code):
    message = "Error"
    if status_code == 429:
        message = "API Key maxed out"
    #return Response(message, status=status_code)
    return create_json_response(message)


def is_error(response):
    return response.status != 200


def get_request_param(request, param_name, is_list = False):
    val_str = request.args.get(param_name.encode('utf-8'))[0].decode('utf-8')
    if is_list:
        return json.loads(val_str)
    else:
        return val_str 

    
def create_json_response(json_obj):
    return response.json(json_obj)


@app.route("/")
def hello(request):
    return "Hello World!"


@app.route("/api/<server>/summoner/<summoner_name>/overview")
async def get_summoner_overview(request, server, summoner_name):
    allow_cors(request)
    url = compose_url("/lol/summoner/v4/summoners/by-name/" + summoner_name, server)
    response = await get_http_response(app, url)
    if is_error(response):
        return get_error_response(response.code)
    json_data = await get_response_json(app, response)
    return create_json_response({k: json_data[k] for k in ["name", "summonerLevel", "profileIconId"]})


@app.route("/api/<server>/summoner/<summoner_name>/account")
async def get_summoner_account_id(request, server, summoner_name):
    allow_cors(request)
    url = compose_url("/lol/summoner/v4/summoners/by-name/" + summoner_name, server)
    response = await get_http_response(app, url)
    if is_error(response):
        return get_error_response(response.code)
    json_data = await get_response_json(app, response)
    return create_json_response({k: json_data[k] for k in ["accountId", "id"]})


@app.route("/api/<server>/account/<account_id>/matchlist")
async def get_matches(request, server, account_id):
    allow_cors(request)
    url = compose_url("/lol/match/v4/matchlists/by-account/" + account_id, server)
    response = await get_http_response(app, url)
    if is_error(response):
        return get_error_response(response.code)
    json_data = await get_response_json(app, response)
    return create_json_response([{**{k: match_obj[k] for k in ["gameId", "lane", "role", "timestamp"]}, 
                     "championName": champion_data.get_champion_name(match_obj["champion"]),
                     "queue": queue_names.get_queue_name(match_obj["queue"])} for match_obj in json_data["matches"]])


@app.route("/api/<server>/summoner/<summoner_id>/champion/mastery")
async def get_champion_mastery(request, server, summoner_id):
    allow_cors(request)
    url = compose_url("/lol/champion-mastery/v4/champion-masteries/by-summoner/" + summoner_id, server)
    response = await get_http_response(app, url)
    if is_error(response):
        return get_error_response(response.code)
    json_data = await get_response_json(app, response)
    return create_json_response([{**{k: champ_obj[k] for k in ["championId", "championLevel", "championPoints"]}, 
                     "championName": champion_data.get_champion_name(champ_obj["championId"])} for champ_obj in json_data[:25]])


@app.route("/api/<server>/match_timeline/<match_id>")
async def get_match_timeline(request, server, match_id):
    allow_cors(request)
    url = compose_url("/lol/match/v4/timelines/by-match/" + match_id, server)
    response = await get_http_response(app, url)
    if is_error(response):
        return get_error_response(response.code)
    json_data = await get_response_json(app, response)
    return create_json_response(timeline_analysis.get_timeline_data(json_data, get_request_param(request, "event"), int(get_request_param(request, "pID"))))


async def fetch_combined_timeline(request, server, account_id, match_ids, event_type):
    combined_timeline = []
    num_matches = 0
    # First, fetch the match details
    
    details_list = await asyncio.gather(*[get_match_details(request, server, match_id) for match_id in match_ids])
    for i, details_json_str in enumerate(details_list):
        print("Number " + str(num_matches), flush=True)
        details_json = json.loads(details_json_str)
        participant_id = match_details.get_participant_id(details_json, account_id)
        if participant_id is None:
            continue
        url = compose_url("/lol/match/v4/timelines/by-match/" + match_ids[i], server)
        match_timeline_response = await get_http_response(app, url)
        if is_error(match_timeline_response):
            return get_error_response(match_timeline_response.code)
        match_timeline_json = await get_response_json(app, match_timeline_response)
        match_events = timeline_analysis.get_timeline_data(match_timeline_json, event_type, participant_id)
        combined_timeline.extend(match_events)
        num_matches += 1
    return create_json_response({"matches": num_matches, "timeline": combined_timeline})


@app.route("/api/<server>/account/<account_id>/combined_timeline")
async def get_combined_timeline(request, server, account_id):
    allow_cors(request)
    print(request.args, flush=True)
    match_ids = [str(matchId) for matchId in get_request_param(request, "matchIDs", True)]
    print(match_ids, flush=True)
    event_type = get_request_param(request, "event")

    return await fetch_combined_timeline(request, server, account_id, match_ids, event_type)


@app.route("/api/<server>/account/<account_id>/full_timeline")
async def get_full_timeline(request, server, account_id):
    allow_cors(request)
    matches_response = get_matches(request, server, account_id)
    if is_error(matches_response):
        return get_error_response(matches_response.code)
    matches = await get_response_json(app, matches_response)
    event_type = get_request_param(request, "event")

    match_ids = [str(match["gameId"]) for match in matches[:20]]
    return await fetch_combined_timeline(request, server, account_id, match_ids, event_type)


@app.route("/api/<server>/match/<match_id>")
async def get_match_details(request, server, match_id):
    allow_cors(request)
    url = compose_url("/lol/match/v4/matches/" + match_id, server)
    response = await get_http_response(app, url)
    if is_error(response):
        return get_error_response(response.code)
    json_data = await get_response_json(app, response)
    return create_json_response(match_details.get_relevant_details(json_data))


def compose_url(url, server):
    return "https://" + region_end_points[server] + url + "?api_key=" + api_key

if __name__ == "__main__":
    app.run("localhost", 5000, workers=2)