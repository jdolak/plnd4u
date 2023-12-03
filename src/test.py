#!/usr/bin/env python3

from func_basic import *
from func_adv import *

netid = "jjenkins"

print("Missing Core Requirements:", db_check_core_requirements(netid), "\n")
print("Missing Major Requirements:", db_check_required_courses(netid), "\n")
print("Missing Electives:", db_check_electives(netid), "\n")