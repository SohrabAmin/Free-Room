import uoftscrapers
import os

utm_courses = []

entries = os.listdir('course_json/')
for i in range(len(entries)):
    if 'H5' in entries[i]:
        utm_courses.append(entries[i])

print(utm_courses)

