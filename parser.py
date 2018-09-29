import html
import requests
from speaker import Speaker
from event import Event
from hackathon import Hackathon
from talk import Talk
from bs4 import BeautifulSoup

BASE_URL = "http://2018.hackerkiste.de/"


class Parser():
    def __init__(self):
        return

    def parse_speakers(self):
        soup = self._cook_yummy_soup()
        speaker_html_elements = soup.find_all("div", attrs={"class": "speaker-content"})
        speaker_list = []
        for elem in speaker_html_elements:
            speaker_list.append(self._parse_speaker(elem).__dict__)
        return speaker_list
    

    def _parse_speaker(self, speaker_elem):
        name_and_company = speaker_elem.h6.text
        name, company = str(name_and_company).split(", ")
        img_src = speaker_elem.previous_sibling.previous_sibling.get("src")
        return Speaker(name, company, BASE_URL + "/" + img_src)


    def parse_events(self):
        soup = self._cook_yummy_soup()
        fday = soup.find("div", attrs={"id": "fday"})
        sday = soup.find("div", attrs={"id": "sday"})
        fday = self._parse_events_of_day(fday, 28)
        sday = self._parse_events_of_day(sday, 29)
        fday.extend(sday)
        event_list = fday
        return event_list
    
    def _parse_events_of_day(self, day_html, day_int):
        childs = self._filter_new_lines(day_html.children)
        event_list = []
        for i in range(0, len(childs), 3):
            time_html = childs[i]
            start_time, end_time = self._datestr_to_iso(time_html.text.strip(), day_int)
            html_item = time_html.next_sibling.next_sibling
            all_h3_titles= html_item.find_all("h3")
            all_h4_details = html_item.find_all("h4")
            all_h6_places = html_item.find_all("h6")
            for i in range(0, len(all_h6_places)):
                title = all_h3_titles[i].text.strip()
                place = all_h6_places[i].text.strip()
                event_type = "Normal"
                try:
                    event_type = all_h3_titles[i].span.text.strip()
                except:
                    pass
                details = "" if event_type is "Normal" else all_h4_details[i].text
                event = Event(title, start_time, end_time, place, event_type, details)
                event_list.append(event.__dict__)
        return event_list

    def parse_talks(self):
        return list(filter(lambda x: x["event_type"]== "Talk", self.parse_events()))
        
    def parse_barcamps(self):
        return list(filter(lambda x: x["event_type"]== "Barcamp", self.parse_events()))

    
    def parse_hackathons(self):
       hackathon_html_list = self._cook_yummy_soup().find_all("div", attrs={"class": "hackathon-submission-item"})
       hackathon_list = []
       for hackathon_html in hackathon_html_list:
           hackathon_list.append(self._parse_hackathon(hackathon_html).__dict__)
       return hackathon_list

    def _parse_hackathon(self, hackathon_html):
        title = hackathon_html.h3.text.strip()
        summary = hackathon_html.next_sibling.next_sibling.text.strip()
        speaker_details = hackathon_html.h4.text.strip()
        return Hackathon(title, summary, speaker_details)


    def _cook_yummy_soup(self) -> BeautifulSoup:
        r = requests.get(BASE_URL).text.encode("latin1").decode("utf-8")
        return BeautifulSoup(r)

    def _filter_new_lines(self, iterable):
        return list(filter(lambda x: x != "\n", iterable))

    def _datestr_to_iso(self, time_str, day):
        import datetime
        if "ab" in time_str:
            _temp, start = time_str.split("ab ")
            start_hours, start_min = start.split(":")
            return datetime.datetime(2018, 9, day, int(start_hours), int(start_min)), None

        start, end = time_str.split(" – ")
        start_hours, start_min = start.split(":")
        end_hours, end_min = end.split(":")
        start_datetime = datetime.datetime(2018, 9, day, int(start_hours), int(start_min))
        end_datetime = datetime.datetime(2018, 9, day, int(end_hours), int(end_min))
        return start_datetime, end_datetime