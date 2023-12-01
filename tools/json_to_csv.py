#!/usr/bin/env python3

import json
import csv

def produce_line(course, course_dict):
    output = ""
    for prereq_major in course_dict:
        for prereq_code in course_dict[prereq_major]:
            output = f'{output}{prereq_major} {prereq_code},'
    return [course, output[:-1]]
        

def main():
    with open("data/json/sp24_extracted_prerequisites.json", encoding='utf-8') as fd:
        json_data = json.load(fd)

    with open("data/csv/sp24_prereqs.csv", "w", newline="") as csvfile:
        writer = csv.writer(csvfile, delimiter=",")

        for course in json_data:
            course_dict = json_data[course]

            if "req1" not in course_dict:
                writer.writerow(produce_line(course, course_dict))
            else:
                for req in course_dict:
                    writer.writerow(produce_line(course, course_dict[req]))
                
                        
            
                


if __name__=="__main__":
    main()