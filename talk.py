#!/bin/python
from event import Event
class Talk(Event):

    def __init__(self, title, time, place, speaker):
        super().__init__(title, time, place)
        self.speaker = speaker