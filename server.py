#!/bin/python
import datetime
from parser import Parser
from flask import Flask, jsonify
from bs4 import BeautifulSoup

app = Flask(__name__)
parser = Parser()

@app.route("/speakers")
def get_speakers():
    speaker_list = parser.parse_speakers()
    return _json_response(speaker_list)

@app.route("/talks")
def get_talks():
    talk_list = parser.parse_talks()
    return _json_response(talk_list)

@app.route("/events")
def get_events():
    event_list = parser.parse_events()
    return _json_response(event_list)
@app.route("/events/current")
def get_current_events():
    all_events = parser.parse_events()
    current_events = []
    current_time = datetime.datetime.now()
    for event in all_events:
        if event["end_time"] == None:
            event["end_time"] = datetime.datetime(2018, 9, event["start_time"].day, 23, 59)
        if event["start_time"] <= current_time <= event["end_time"]:
            current_events.append(event)
    return _json_response(current_events)


@app.route("/hackathons")
def get_hackathons():
    hackathon_list = parser.parse_hackathons()
    return _json_response(hackathon_list)

@app.route("/barcamps")
def get_barcamps():
    barcamp_list = parser.parse_barcamps()
    return _json_response(barcamp_list)

def _json_response(payload):
    resp = jsonify(payload)
    resp.status_code = 200
    return resp