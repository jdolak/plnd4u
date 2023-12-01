#!/usr/bin/env python3

from func_basic import *

course = "AME 30331"

print("Description:", db_show_description((course)))
print("Credits:", db_show_credits((course)))
print("Core Requirements Fulfilled:", db_show_core_reqs((course)))
print("Details:", db_show_section_details((course)))
print("Corequisites:", db_show_coreqs((course)))
print("Prerequisites:", db_show_prereqs((course)))
