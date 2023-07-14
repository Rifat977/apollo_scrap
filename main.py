import requests
import json
import csv
from flatten_json import flatten
from urllib.parse import urlparse, parse_qs, unquote
import subprocess


url = input("Enter the URL: ")
parsed_url = urlparse(url)
query_params = parse_qs(parsed_url.query, keep_blank_values=True)


fragment_params = {}
if parsed_url.fragment:
    for item in parsed_url.fragment.split('&'):
        key_value = item.split('=')
        if len(key_value) == 2:
            key, value = key_value
            key = unquote(key).rstrip('[]')
            value = unquote(value)
            if key in fragment_params:
                fragment_params[key].append(value)
            else:
                fragment_params[key] = [value]

api_key = "aiYbdwT0rGO_FEQOJTs2og"

payload = {
    "api_key": api_key,
    "page": 1,
    "per_page": 25,
    "display_mode": "explorer_mode",
    "show_suggestions": False,
    "ui_finder_random_seed": "sl6dq24o97",
    "cacheKey": 1686239974184
}

for key, values in query_params.items():
    key = unquote(key).rstrip('[]')
    values = [unquote(value) for value in values]
    payload[key] = values

for key, values in fragment_params.items():
    payload[key] = values

source = "https://api.apollo.io/v1/mixed_people/search"

csv_file = 'mixed_data.csv'

headers = {
    "Content-Type": "application/json",
    "Cache-Control": "no-cache"
}

all_people = []
needed_data = int(input("Enter the number of data needed: "))
data_count = 0

data_count = 0
payload['page'] = 1
while data_count < needed_data:
    response = requests.post(source, data=json.dumps(payload), headers=headers)

    if response.status_code == 200:
        response_data = response.json()
        retrieved_people = response_data['people']
        all_people.extend(retrieved_people)
        data_count += len(retrieved_people)
        print(f"Retrieved data from page {payload['page']}")
        payload['page'] += 1
    elif response.status_code == 422:
        print("No more data available.")
        break
    else:
        print(f"Error: Request failed for status code {response.status_code}")
        break

flattened_people = [flatten(person) for person in all_people]

field_names = set().union(*[person.keys() for person in flattened_people])

with open(csv_file, 'w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=field_names)
    writer.writeheader()
    writer.writerows(flattened_people)


subprocess.run(['python', 'sort.py'])
