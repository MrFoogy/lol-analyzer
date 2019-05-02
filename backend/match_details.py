import champion_data

def get_relevant_details(json_data):
    teams = {}
    teams["red"] = {"participants": []}
    teams["blue"] = {"participants": []}
    for team_json in json_data["teams"]:
        stats = {}
        stats["win"] = team_json["win"]
        if team_json["teamId"] == 100:
            teams["blue"]["stats"] = stats
        else:
            teams["red"]["stats"] = stats
    for participant_json in json_data["participants"]:
        summonerName = ""
        for player_json in json_data["participantIdentities"]:
            if player_json["participantId"] == participant_json["participantId"]:
                summonerName = player_json["player"]["summonerName"]
        participant = {"participantId": participant_json["participantId"],
                       "summonerName": summonerName, 
                       "championName": champion_data.get_champion_name(participant_json["championId"]),
                       "lane": participant_json["timeline"]["lane"],
                       "role": participant_json["timeline"]["role"],
                       "spell1Id": participant_json["spell1Id"],
                       "spell2Id": participant_json["spell2Id"],
                       "kills": participant_json["stats"]["kills"],
                       "deaths": participant_json["stats"]["deaths"],
                       "assists": participant_json["stats"]["assists"],
                       "cs": participant_json["stats"]["totalMinionsKilled"]}
        if participant_json["teamId"] == 100:
            teams["blue"]["participants"].append(participant)
        else:
            teams["red"]["participants"].append(participant)
    return {"teams": teams, "duration": json_data["gameDuration"]}

