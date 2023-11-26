#!/usr/bin/env python3

import json
import csv

CORE_REQS = set(["WKAL", "WKCD", "WKDT", "WKFP", "WKFT", "WKHI", "WKIN", "WKLC", "WKQR", "WKSP", "WKSS", "WKST", "WRIT", "WRRH", "USEM"])

def main():
    with open("data/json/fa23_data.json", encoding='utf-8') as fd:
        json_data = json.load(fd)

    with open("data/csv/fa23_attributes.csv", "w", newline="") as csvfile:
        writer = csv.writer(csvfile, delimiter=",")

        for course in json_data:
            ad = json_data[course]["attribute_description"]

            if ad == "":
                continue

            for req in CORE_REQS:
                if req in ad:
                    writer.writerow([f'{course}', f'{req}'])

if __name__=="__main__":
    main()