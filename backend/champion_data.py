import json
champions_json = []

with open("champion.json", encoding="utf8") as champions_file:
    champions_json = json.load(champions_file)["data"]

def get_champion_name(champ_id):
    for champ_name in champions_json:
        if champions_json[champ_name]["key"] == str(champ_id):
            return champ_name
    return "Ekko"