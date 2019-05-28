import champion_data
import queue_names

def filter_matches(json_data, queues, champions):
    filtered_matches = [match for match in json_data["matches"] if (match["queue"] in queues and (not champions or match["champion"] in champions))]
    return [{**{k: match_obj[k] for k in ["gameId", "lane", "role", "timestamp"]},
             "championName": champion_data.get_champion_name(match_obj["champion"]),
             "queue": queue_names.get_queue_name(match_obj["queue"])} for match_obj in filtered_matches]
