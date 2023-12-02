#!/usr/bin/env python3

from func_basic import *
from flask import jsonify

course_code = "KSGA 10002"

desc = db_show_description(course_code)
credits = db_show_credits(course_code)
core_reqs = db_show_core_reqs(course_code)
recent_sems = db_show_semesters(course_code)
profs = db_show_profs(course_code)
meeting_times = db_show_meeting_times(course_code)
coreqs = db_show_coreqs(course_code)
prereqs = db_show_prereqs(course_code)

print(desc, credits, core_reqs, recent_sems, profs, meeting_times, coreqs, prereqs)

