#!/usr/bin/env python3

import json
import csv

def convert(source, dest):
    with open(source, encoding='utf-8') as fd:
        json_data = json.load(fd)

    with open(dest, "w", newline="") as csvfile:
        writer = csv.writer(csvfile, delimiter="\t")

        for course in json_data:
            desc = " ".join(json_data[course].splitlines())
            desc = desc.replace("\t", " ")
            writer.writerow([f'{course}', f'{desc}'])
        
def main():
    convert("data/descriptions.json", "data/descriptions.tsv")

if __name__=="__main__":
    main()