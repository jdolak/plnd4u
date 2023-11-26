#!/usr/bin/env python3

import json
import csv

def convert(source, dest):
    with open(source, encoding='utf-8') as fd:
        json_data = json.load(fd)

    with open(dest, "w", newline="") as csvfile:
        writer = csv.writer(csvfile, delimiter=",")

        for course in json_data:
            coreq = json_data[course]
            writer.writerow([f'{course}', f'{coreq}'])
        
def main():
    convert("data/credits.json", "data/credits.csv")

if __name__=="__main__":
    main()