from enum import Enum

class Event():
    def __init__(self, title, start_time, end_time, place, event_type, details):
        self.title = title
        self.start_time = start_time
        self.end_time = end_time
        self.place = place
        self.event_type = event_type
        self.details = details
