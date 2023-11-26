#!/usr/bin/env python3

import json
import csv

def main():
    with open("data/json/sp24_overview.json", encoding='utf-8') as fd:
        json_data = json.load(fd)
        overview = json_data["results"]

    with open("data/csv/sp24_overview.csv", "w", newline="") as csvfile:
        writer = csv.writer(csvfile, delimiter=",")
        writer.writerow(["code","title","crn","meets","professor","start_date"])

        for cd in overview:
            writer.writerow([cd["code"],cd["title"],cd["crn"],cd["meets"],cd["instr"],cd["start_date"]])

if __name__=="__main__":
    main()