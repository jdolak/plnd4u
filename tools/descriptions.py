#!/usr/bin/env python3

import requests
import json
from concurrent.futures import ThreadPoolExecutor

# Base URL and endpoint
URL = "https://classsearch.nd.edu/api/?page=fose&route=details"

# Headers
HEADERS = {
    "accept": "application/json, text/javascript, */*; q=0.01",
    "accept-language": "en-US,en;q=0.9",
    "content-type": "application/json",
    "sec-ch-ua": "\"Google Chrome\";v=\"119\", \"Chromium\";v=\"119\", \"Not?A_Brand\";v=\"24\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"macOS\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "x-requested-with": "XMLHttpRequest",
}


def fetch_description(code):
    body = {
        "group": f"code:{code}",
        "key": "",
        "srcdb": "202320",
    }
    response = requests.post(URL, headers=HEADERS, json=body)
    if response.status_code == 200:
        response_data = json.loads(response.text)
        return code, response_data.get('description', 'No Description')
    else:
        return code, None


def get_codes():
    with open('data.json') as json_file:
        data = json.load(json_file)
    return [c['code'] for c in data['results']]


def get_descriptions():
    codes = get_codes()
    data = {}

    with ThreadPoolExecutor(max_workers=20) as executor:
        results = executor.map(fetch_description, codes)

    for code, description in results:
        if description:
            data[code] = description
        else:
            print(f'Failed to fetch data or No Description found for {code}...')

    with open('descriptions.json', 'w') as file:
        json.dump(data, file)


def main():
    get_descriptions()


if __name__ == '__main__':
    main()
