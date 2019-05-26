def is_correct_event_type(event_type_param, data_event_type):
    if event_type_param == "kill":
        return data_event_type == "CHAMPION_KILL"
    if event_type_param == "death":
        return data_event_type == "CHAMPION_KILL"
    if event_type_param == "assist":
        return data_event_type == "CHAMPION_KILL"
    if event_type_param == "wardplace":
        return data_event_type == "WARD_PLACED"
    if event_type_param == "wardkill":
        return data_event_type == "WARD_KILL"


def get_event_types():
    return ["kill", "death", "assist"]


def get_event_stats_types():
    return ["kill", "death", "assist", "wardplace", "wardkill"]


def get_data_stats_types():
    return ["gold", "cs"]


def get_stats_types():
    return get_event_stats_types() + get_data_stats_types()


def get_stat_data_name(stat_type):
    stat_name_conversions = {"gold": "totalGold", "cs": "minionsKilled"}
    return stat_name_conversions[stat_type]


def is_correct_participant(participant_id, event_type, event_data):
    if event_type == "kill":
        return participant_id == event_data["killerId"]
    if event_type == "death":
        return participant_id == event_data["victimId"]
    if event_type == "assist":
        return participant_id in event_data["assistingParticipantIds"]
    if event_type == "wardplace":
        return participant_id == event_data["creatorId"]
    if event_type == "wardkill":
        return participant_id == event_data["killerId"]


def get_empty_timeline():
    return {"events": {event_type: [] for event_type in get_event_types()}, "stats": []}


def combine_timelines(match_timelines):
    combined_timeline = get_empty_timeline()
    for match_timeline in match_timelines:
        match_events = match_timeline["events"]
        for event_type in match_events:
            combined_timeline["events"][event_type].extend(match_events[event_type])
    last_timestamp = max([timeline["stats"][-1]["timestamp"] for timeline in match_timelines]) 
    millis = 0
    combined_stats = []
    # Store how many timelines where added to constitute each new summed frame
    num_contributors = {}
    # Compute average of stats
    # Add 10000 to have a safety margin for the drift in millis seen in the timeline timestamps
    while (millis < last_timestamp + 10000):
        new_stats_entry = {stat_name: 0 for stat_name in get_stats_types()}
        new_stats_entry['timestamp'] = millis
        num_contributors[millis] = 0
        # For each timeline, find the corresponding timestamp and add the values
        for match_timeline in match_timelines:
            for stats_entry in match_timeline["stats"]:
                if abs(stats_entry["timestamp"] - millis) < 10000:
                    for stat_name in get_stats_types():
                        new_stats_entry[stat_name] += stats_entry[stat_name]
                    num_contributors[millis] += 1
                    break
        combined_stats.append(new_stats_entry)
        # Match timelines use one minute intervals
        millis += 60000
    for stats_entry in combined_stats:
        for stat_name in get_stats_types():
            stats_entry[stat_name] /= num_contributors[stats_entry["timestamp"]]
        
    combined_timeline["stats"] = combined_stats
    return combined_timeline

def get_timeline_data(timeline_json, participant_id):
    timeline = get_empty_timeline()
    event_stats_counter = {event_stat_name: 0 for event_stat_name in get_event_stats_types()}
    for frame in timeline_json["frames"]:
        for event in frame["events"]:
            for event_type in get_event_types():
                if is_correct_event_type(event_type, event["type"]) and is_correct_participant(participant_id, event_type, event):
                    timeline["events"][event_type].append({"position": event["position"]})
            for event_stat_type in get_event_stats_types():
                if is_correct_event_type(event_stat_type, event["type"]) and is_correct_participant(participant_id, event_stat_type, event):
                    event_stats_counter[event_stat_type] += 1
        stats_entry = {"timestamp": frame["timestamp"]}
        for data_stat_type in get_data_stats_types():
            stats_entry[data_stat_type] = frame["participantFrames"][str(participant_id)][get_stat_data_name(data_stat_type)]
        for event_stat_type in get_event_stats_types():
            stats_entry[event_stat_type] = event_stats_counter[event_stat_type]
        timeline["stats"].append(stats_entry)
        
    return timeline
