import requests
import json
import csv
from flatten_json import flatten

url = "https://api.apollo.io/v1/mixed_people/search"
csv_file = 'mixed_data.csv'

headers = {
    "Content-Type": "application/json",
    "Cache-Control": "no-cache"
}

all_people = []
needed_data = int(input("Enter the number of data needed: "))
data_count = 0

api_key = "YEG6pQpChQnaY0yHfisbpw"

organization_keyword_tags = [
    "nursing home",
    "nursing homes",
    "assisted living",
    "retirement home",
    "memory care",
    "retirement community"
]

payload = {
    "api_key": api_key,
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

for organization_keyword_tag in organization_keyword_tags:
    payload["organization_keyword_tags"] = [organization_keyword_tag]
    data_count = 0
    payload['page'] = 1
    while data_count < needed_data:
        response = requests.post(url, data=json.dumps(payload), headers=headers)

        if response.status_code == 200:
            response_data = response.json()
            retrieved_people = response_data['people']
            all_people.extend(retrieved_people)
            data_count += len(retrieved_people)
            print(f"Retrieved data from page {payload['page']}")
            payload['page'] += 1
        elif response.status_code == 422:
            print(f"No more data available for organization keyword tag: {organization_keyword_tag}")
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
