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
        #self.events = json['meeting_sections']
        self.events = []
        for event in json['meeting_sections']:
            self.events.append(Event(event))


class Event:
    """
    A UTM Course Meeting Section
    """
    def __init__(self, json: dict):
        if len(json['times']) != 0:
            self.section = json['code']
            self.location = json['times'][0]['location']
            self.day = json['times'][0]['day']
            self.start_time = json['times'][0]['start']
            self.end_time = json['times'][0]['end']


if __name__ == '__main__':

    # Add Course Names
    course_dir = os.listdir('course_json/')
    utm_courses = [course for course in course_dir if 'H5' in course]

    # Create Course Objects
    courses = []
    for course in utm_courses:
        file = open('course_json/' + course)
        str_json = file.readline()
        courses.append(Course(json.loads(str_json)))

    #print(courses[2].events)
    print(courses[2].events[0])
    for i in range(len(courses[2].events)):
        print('-------------------------------')
        print(courses[2].name)
        print(courses[2].events[i].section)
        print(courses[2].events[i].location)
        print(courses[2].events[i].day)
        print(courses[2].events[i].end_time)
        print(courses[2].events[i].start_time)
        print('-------------------------------')









    #print(courses[2].events[0]['times'])
    #[{'day': 'FRIDAY', 'start': 39600, 'end': 46800, 'duration': 7200, 'location': 'CC 1080'}]



