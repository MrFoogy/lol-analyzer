queue_names = {
    400: "Normal (Draft Pick)",
    420: "Ranked Solo/Duo",
    430: "Normal (Blind Pick)",
    440: "Ranked Flex",
    450: "ARAM",
    460: "Twisted Treeline (Normal)",
    470: "Twisted Treeline (Ranked)",
    900: "ARURF",
    1020: "One for All",
    1200: "Nexus Blitz"
}

def get_queue_name(queue_id):
    if queue_id in queue_names: 
        return queue_names[queue_id]
    return "Special Mode"