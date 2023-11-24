#!/usr/bin/env python3

import json
import csv

with open("data/descriptions.json", encoding='utf-8') as fd:
    json_data = json.load(fd)

with open("data/descriptions.tsv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile, delimiter="\t")

    for course in json_data:
        desc = " ".join(json_data[course].splitlines())
        desc = desc.replace("\t", " ")
        writer.writerow([f'{course}', f'{desc}'])