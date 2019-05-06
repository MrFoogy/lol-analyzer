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


def get_timeline_data(timeline_json, event_type, participant_id):
    res = []
    for frame in timeline_json["frames"]:
        for event in frame["events"]:
            if is_correct_event_type(event_type, event["type"]) and is_correct_participant(participant_id, event_type, event):
                res.append({"position": event["position"]})
    return res
