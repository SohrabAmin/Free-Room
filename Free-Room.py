import os
import json
from md_Generator import create_md_table
import matplotlib


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
            for subevent in event['times']:
                self.events.append(Event(subevent, json['term'][0:4], json['code']))


class Event:
    """
    A UTM Course Meeting Section
    """
    def __init__(self, json: dict, term: str, code: str):
        self.full_year = 'Y' == code[-1]
        self.term = term
        self.code = code
        self.location = json['location']
        self.day = json['day']
        self.start_time = json['start']//3600
        self.end_time = json['end']//3600


class Building:
    """
    A UTM Building
    """
    def __init__(self, name):
        self.name = name
        self.rooms = []

    def __repr__(self):
        return self.name


class Room:
    """
    A UTM Room in a Building.
    """
    def __init__(self, number):
        self.number = number
        self.schedule = {}


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
        c = Course(json.loads(str_json))
        courses.append(c)

    # Create and Populate Rooms Map
    Buildings = {}
    Rooms = {}

    for course in courses:
        for event in course.events:
            if event.term == '2020' or event.full_year:
                if event.location not in Rooms:
                    Rooms[event.location] = Room(event.location)
                    Rooms[event.location].schedule[event.day] = [[event.start_time, event.end_time]]
                elif event.day not in Rooms[event.location].schedule:
                    Rooms[event.location].schedule[event.day] = [[event.start_time, event.end_time]]
                else:
                    Rooms[event.location].schedule[event.day].append([event.start_time, event.end_time])

    # Merge Intervals in Schedule
    for room in Rooms:
        for day in Rooms[room].schedule:
            Rooms[room].schedule[day] = merge_intervals(Rooms[room].schedule[day])


    # Populate Buildings Map
    for room in Rooms:
        if Rooms[room].number[0:2] not in Buildings:
            Buildings[Rooms[room].number[0:2]] = Building(Rooms[room].number[0:2])
            Buildings[Rooms[room].number[0:2]].rooms.append(Rooms[room])
        else:
            Buildings[Rooms[room].number[0:2]].rooms.append(Rooms[room])


    # Print all Rooms and Times
    for building in Buildings:
        for room in Buildings[building].rooms:
            print(room.number, room.schedule)


    # Add Data to README.md
    # table2 = [['Davis', '2062', '2059'],
    #          ['8:00', 'x', ' '],
    #          ['9:00', 'x', 'x'],
    #          ['10:00', 'x', 'x']]
    #
    # file = open('Assets/markdown.md', 'r+')
    # file.truncate(0)
    # file.write(create_md_table(table2))
    #
    # table = [['00'],
    #          ['08:00'],
    #          ['09:00'],
    #          ['10:00'],
    #          ['11:00'],
    #          ['12:00'],
    #          ['13:00'],
    #          ['14:00'],
    #          ['15:00'],
    #          ['16:00'],
    #          ['17:00'],
    #          ['18:00'],
    #          ['19:00'],
    #          ['20:00'],
    #          ['21:00'],
    #          ['22:00']]
    #
    # for building in Buildings:
    #     for room in Buildings[building].rooms:
    #         for schedule in room.schedule:
    #             if schedule == 'MONDAY' and room.number[0:2] == 'IB':
    #                 #print(room.number, room.schedule['MONDAY'])
    #                 for row in range(len(table)):
    #                     for times in room.schedule['MONDAY']:
    #                         if int(table[row][0][0:2]) in range(int(times[0]), int(times[1])):
    #                             table[row].append('x')
    #
    # print(table)



