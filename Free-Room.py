from datetime import datetime
import os
import json


class Course:
    """
    A UTM Course
    """
    def __init__(self, json: dict):
        """
        Instantiate a UTM Course.
        """
        self.id = json['id']
        self.code = json['code']
        self.name = json['name']
        self.term = json['term']
        self.events = []
        for event in json['meeting_sections']:
            if len(event['times']) != 0:
                self.events.append(Event(event, json['term'][0:4], json['code']))


class Event:
    """
    A UTM Course Meeting Section
    """
    def __init__(self, json: dict, term: str, code: str):
        self.term = term
        self.code = code
        self.section = json['code']
        self.location = json['times'][0]['location']
        self.day = json['times'][0]['day']
        self.start_time = datetime.strptime(str(int(json['times'][0]['start'])//3600), '%H').strftime('%I:%M %p')
        self.end_time = datetime.strptime(str(int(json['times'][0]['end'])//3600), '%H').strftime('%I:%M %p')


class Building:
    """
    A UTM Building
    """
    def __init__(self, name):
        self.name = name
        self.rooms = []


class Room:
    """
    A UTM Room in a Building.
    """
    def __init__(self, number):
        self.number = number
        self.schedule = []


if __name__ == '__main__':

    # Add Course Names
    course_dir = os.listdir('course_json/')
    utm_courses = [course for course in course_dir if 'H5' in course]

    # Create and Populate Course Objects
    courses = []
    for course in utm_courses:
        file = open('course_json/' + course)
        str_json = file.readline()
        courses.append(Course(json.loads(str_json)))

    # Create and Populate Building and Room
    Buildings = {}
    Rooms = {}

    for course in courses:
        for event in course.events:
            if event.term == '2020':
                if event.location not in Rooms:
                    Rooms[event.location] = Room(event.location)
                else:
                    Rooms[event.location].schedule.append(event.code +' '+event.start_time+'-'+event.end_time)

    for room in Rooms:
        print(room, Rooms[room].schedule)


