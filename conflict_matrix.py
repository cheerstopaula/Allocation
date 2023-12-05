import numpy as np
import datetime


def gen_conflict_matrix(items):

    conflict_mat = np.zeros((1, len(items)))
    constraints = np.zeros((1, 1))
    courses = []
    days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri']
    slots = ['08:00 AM', '08:15 AM', '08:30 AM', '08:45 AM', '09:00 AM', '09:15 AM',
             '09:30 AM', '09:45 AM', '10:00 AM', '10:15 AM', '10:30 AM', '10:45 AM',
             '11:00 AM', '11:15 AM', '11:30 AM', '11:45 AM', '12:00 PM', '12:15 PM',
             '12:30 PM', '12:45 PM', '01:00 PM', '01:15 PM', '01:30 PM', '01:45 PM',
             '02:00 PM', '02:15 PM', '02:30 PM', '02:45 PM', '03:00 PM', '03:15 PM',
             '03:30 PM', '03:45 PM', '04:00 PM', '04:15 PM', '04:30 PM', '04:45 PM',
             '05:00 PM', '05:15 PM', '05:30 PM', '05:45 PM', '06:00 PM', '06:15 PM',
             '06:30 PM', '06:45 PM', '07:00 PM', '07:15 PM', '07:30 PM', '07:45 PM',
             '08:00 PM', '08:15 PM', '08:30 PM', '08:45 PM', '09:00 PM', '09:15 PM']

    for day in days:
        for slot in slots:
            slot = datetime.datetime.strptime(slot, "%I:%M %p")
            day_slot_row = np.zeros(len(items))
            for i in range(len(items)):
                item_times = [datetime.datetime.strptime(time, "%I:%M %p") for time in items[i].time.split(" - ")]
                item_days = [d for d in items[i].days.split(' ')]
                if (item_times[0]-datetime.timedelta(minutes=14) <= slot) and (slot < item_times[1]):
                    if day in item_days:
                        day_slot_row[i] = 1
            if np.sum(day_slot_row) > 1:
                conflict_mat = np.vstack((conflict_mat, day_slot_row))
                constraints = np.vstack((constraints, [1]))

    for item in items:
        if item.course not in courses:
            courses.append(item.course)

    """Cannot be in same course, multiple different sections"""
    for course in courses:                          # new row in preference matrix for each course
        course_row = np.zeros(len(items))         # new entry in constraints for each course
        for i in range(len(items)):
            if (course == items[i].course):
                course_row[i] = 1
        if np.sum(course_row) > 1:
            conflict_mat = np.vstack((conflict_mat, course_row))
            constraints = np.vstack((constraints, [1]))

    return conflict_mat, constraints
