import requests
import json
import csv
import subprocess
from flatten_json import flatten
# from proxy import scrape_proxy_list, test_proxy

url = "https://api.apollo.io/v1/mixed_people/search"
csv_file = 'mixed_data.csv'

person_titles = [
    "nursing home",
    "nursing homes",
    "assisted living",
    "retirement home",
    "memory care",
    "retirement community"
]



headers = {
    "Content-Type": "application/json",
    "Cache-Control": "no-cache"
}

all_people = []
needed_data = int(input("Enter the number of data needed: "))
data_count = 0

api_key = "ZUqZYPkbtWpl6yAy2ORLrQ"

for person_title in person_titles:
    page = 1
    while data_count < needed_data:
        payload = {
            "api_key" : api_key,
            "page": page,
            "organization_keyword_tags": person_titles,
            "organization_num_employees_ranges": ["1,10", "11,20", "21,50"],
            "person_locations": ["United States"],
            "included_organization_keyword_fields": ["tags", "name"],
            "page": 1,
            "person_titles": ["marketing"],
            "prospected_by_current_team": ["no"],
            "display_mode": "explorer_mode",
            "per_page": 25,
            "context": "people-index-page",
            "show_suggestions": False,
            "ui_finder_random_seed": "sl6dq24o97",
            "cacheKey": 1686239974184
        }
        response = requests.post(url, data=json.dumps(payload), headers=headers)

        if response.status_code == 200:
            response_data = response.json()
            retrieved_people = response_data['people']
            all_people.extend(retrieved_people)
            data_count += len(retrieved_people)
            print(f"Retrieved data from page {page}")
            page += 1
        elif response.status_code == 422:
            print(f"Last page retrieved: {page-1}")
            break
        else:
            print(f"Error: Request failed for status code {response.status_code}")
            page += 1
            break

flattened_people = [flatten(person) for person in all_people]

field_names = set().union(*[person.keys() for person in flattened_people])

with open(csv_file, 'w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=field_names)
    writer.writeheader()
    writer.writerows(flattened_people)

