def get_all_kills(timeline_json):
    res = []
    for frame in timeline_json["frames"]:
        for event in frame["events"]:
            if event["type"] == "CHAMPION_KILL":
                res.append({"position": event["position"]})
    return res
