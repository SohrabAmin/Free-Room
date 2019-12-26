import os
import json
from datetime import datetime


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
        self.start_time = json['times'][0]['start']//3600
        self.end_time = json['times'][0]['end']//3600
        #self.start_time = datetime.strptime(str(int(json['times'][0]['start'])//3600), '%H').strftime('%I:%M %p')
        #self.end_time = datetime.strptime(str(int(json['times'][0]['end'])//3600), '%H').strftime('%I:%M %p')


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


def merge_intervals(arr):

    # Sorting based on the increasing order
    # of the start intervals
    arr.sort(key=lambda x: x[0])

    # array to hold the merged intervals
    m = []
    s = -10000
    max = -100000
    for i in range(len(arr)):
        a = arr[i]
        if a[0] > max:
            if i != 0:
                m.append([s, max])
            max = a[1]
            s = a[0]
        else:
            if a[1] >= max:
                max = a[1]

    if max != -100000 and [s, max] not in m:
        m.append([s, max])
    # print("The Merged Intervals are :", end=" ")
    # for i in range(len(m)):
    #     print(m[i], end=" ")
    return m


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
                    Rooms[event.location].schedule.append([event.start_time, event.end_time])

    # Merge Intervals in Schedule
    for room in Rooms:
        Rooms[room].schedule = merge_intervals(Rooms[room].schedule)

    # Print all Rooms and Times
    for room in Rooms:
        print(room, Rooms[room].schedule)