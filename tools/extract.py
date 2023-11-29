#!/usr/bin/env python3

import re
import json
import sys
from collections import defaultdict

GROUP_PATTERN = r'\([^)]*\)'
COURSE_PATTERN = r"([A-Z]+\s\d+)"
REQ_PATTERN = r"Prerequisite.+?</p"

# Functions


def _extract():
    data = {}
    read, write = sys.argv[1:]

    with open(read, "r") as file:
        json_data = json.load(file)

        for course in json_data:
            prerequisites = defaultdict(list)
            restrictions = json_data[course]

            requisite_string = re.search(REQ_PATTERN, restrictions)

            if not requisite_string:
                continue

            requisite_string = requisite_string.group()
            
            if re.search(GROUP_PATTERN, requisite_string):
                groups = re.findall(GROUP_PATTERN, requisite_string)
                inner = {}
                for i, group in enumerate(groups):
                    group = group.replace("(", "")
                    group = group.replace(")", "")
                    courses = group.split(",")
                    
                    curr = courses[0].split()[0]
                    inner_courses = defaultdict(list)
                    for crs in courses:
                        
                        crs = crs.strip()
                        if 'or' in crs:
                            crs = [c.strip() for c in crs.split('or')]
                            for c in crs:
                                if not re.search(r'[A-Z]+', c):
                                    inner_courses[curr].append(c[:-12] if 'sup' in c else c)
                                else:
                                    curr = c.split()[0]
                                    inner_courses[curr].append(c.split()[1][:-12] if 'sup' in c else c.split()[1])

                        else:
                            if not re.search(r'[A-Z]+', crs):
                                inner_courses[curr].append(crs[:-12] if 'sup' in crs else crs)
                            else:
                                curr = crs.split()[0]
                                inner_courses[curr].append(crs.split()[1] if 'sup' in crs else crs.split()[1])

                    req = "req" + str(i + 1)
                    
                    inner[req] = inner_courses

                
                prerequisites = inner
            else:
                codes = re.findall(COURSE_PATTERN, restrictions)

                for code in codes:
                    subject, number = code.split()
                    prerequisites[subject].append(number)

            if prerequisites:
                data[course] = prerequisites

    with open(write, "w") as file:
        json.dump(data, file)


# Main Execution

if __name__ == "__main__":
    _extract()
