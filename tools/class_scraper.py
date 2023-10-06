#!/usr/bin/env python3

import requests
from seleniumwire import webdriver
from selenium.webdriver.common.by import By
import time
import json
import csv

URL = "https://classsearch.nd.edu/"
API_URL = "https://classsearch.nd.edu/api/?page=fose&route=search&camp=M&stat=A%2CF"

HEADERS = {
    "accept": "application/json, text/javascript, */*; q=0.01",
    "content-type": "application/json",
    "origin": "https://classsearch.nd.edu",
    "referer": "https://classsearch.nd.edu/",
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
    "x-requested-with": "XMLHttpRequest",
}

DATA = json.dumps(
    {
        "other": {"srcdb": "202310"},
        "criteria": [
            {"field": "camp", "value": "M"},
            {"field": "stat", "value": "A,F"},
        ],
    }
)

# Functions


def parse(data):
    results = data["results"]
    with open("data.csv", "w") as file:
        writer = csv.writer(file)

        field = ["code", "title", "crn", "meets", "professor", "start_date"]
        writer.writerow(field)

        for result in results:
            writer.writerow(
                [
                    result["code"],
                    result["title"],
                    result["crn"],
                    result["meets"],
                    result["instr"],
                    result["start_date"],
                ]
            )


# Main Execution


def main():
    driver = webdriver.Chrome()

    try:
        driver.get(URL)

        search = driver.find_element(By.ID, "search-button")
        search.click()

        time.sleep(5)

        response = requests.post(API_URL, headers=HEADERS, data=DATA)

        if response.headers["Content-Type"] == "application/json":
            json_data = response.json()

            with open("data.json", "w") as file:
                json.dump(json_data, file)

            parse(json_data)

        else:
            print("Response is not JSON.")

    finally:
        driver.quit()


if __name__ == "__main__":
    main()
