import requests
import json
import csv
import subprocess
from flatten_json import flatten

url = "https://api.apollo.io/v1/mixed_people/search"
csv_file = 'mixed_data.csv'

person_titles = ['Chief Executive Officer (CEO)', 'Chief Financial Officer (CFO)', 'Chief Operating Officer (COO)', 'Human Resources Manager', 'Marketing Director', 'Sales Manager', 'IT Project Manager', 'Software Engineer', 'Data Analyst', 'Graphic Designer', 'Customer Service Representative', 'Account Manager', 'Financial Analyst', 'Operations Manager', 'Content Writer', 'Product Manager', 'Business Development Manager', 'Research Scientist', 'Quality Assurance Engineer', 'Social Media Manager', 'Procurement Specialist', 'Web Developer', 'Systems Administrator', 'HR Generalist', 'Sales Associate', 'IT Support Specialist', 'Event Coordinator', 'Project Coordinator', 'Financial Controller', 'Marketing Coordinator', 'Public Relations Specialist', 'UX/UI Designer', 'Database Administrator', 'Supply Chain Manager', 'Operations Analyst', 'Copywriter', 'Accountant', 'Investment Analyst', 'Logistics Coordinator', 'Customer Success Manager', 'Business Analyst', 'Technical Support Engineer', 'Digital Marketing Specialist', 'Network Engineer', 'Recruitment Specialist', 'Brand Manager', 'Market Research Analyst', 'Software Developer', 'Operations Supervisor', 'Administrative Assistant', 'Data Scientist', 'Sales Representative', 'Project Manager', 'IT Manager', 'Content Manager', 'Financial Planner', 'Operations Coordinator', 'Social Media Specialist', 'Procurement Manager', 'Web Designer', 'Systems Analyst', 'HR Assistant', 'Marketing Assistant', 'Customer Support Specialist', 'Event Planner', 'Business Development Representative', 'Research Analyst', 'Quality Control Inspector', 'SEO Specialist', 'Network Administrator', 'Inventory Manager', 'Data Entry Clerk']

api_key = "LYnrNuerHa1JM7jtirPAdQ"
per_page = 50

headers = {
    "Content-Type": "application/json",
    "Cache-Control": "no-cache"
}

all_people = []
needed_data = int(input("Enter the number of data needed: "))
data_count = 0

for person_title in person_titles:
    page = 1
    while data_count < needed_data:
        payload = {
            "api_key": api_key,
            "page": page,
            "per_page": per_page,
            "person_titles": [person_title]
        }
        response = requests.post(url, data=json.dumps(payload), headers=headers)

        if response.status_code == 200:
            response_data = response.json()
            retrieved_people = response_data['people']
            all_people.extend(retrieved_people)
            data_count += len(retrieved_people)
            print(f"Retrieved data for '{person_title}' from page {page}")
            page += 1
        elif response.status_code == 422:
            print(f"Reached end of pages for '{person_title}'. Last page retrieved: {page-1}")
            break
        else:
            print(f"Error: Request failed for '{person_title}' with status code {response.status_code}")
            page += 1
            continue

flattened_people = [flatten(person) for person in all_people]

field_names = set().union(*[person.keys() for person in flattened_people])

with open(csv_file, 'w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=field_names)
    writer.writeheader()
    writer.writerows(flattened_people)

