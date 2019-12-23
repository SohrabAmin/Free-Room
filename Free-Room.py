import os
import json


class Course:
    """
    A UTM Course
    """
    def __init__(self, json):
        self.id = json['id']
        self.code = json['code']
        self.name = json['name']
        self.term = json['term']
        self.meeting_sections = json['meeting_sections']


if __name__ == '__main__':

    course_dir = os.listdir('course_json/')
    utm_courses = [course for course in course_dir if 'H5' in course]

    courses = []
    for course in utm_courses:
        file = open('course_json/' + course)
        str_json = file.readline()
        courses.append(Course(json.loads(str_json)))




