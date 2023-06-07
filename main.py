import requests
import json
import csv
import subprocess
from flatten_json import flatten
from proxy import scrape_proxy_list, test_proxy

url = "https://api.apollo.io/v1/mixed_people/search"
csv_file = 'mixed_data.csv'

# person_titles = ['Chief Executive Officer (CEO)', 'Chief Financial Officer (CFO)', 'Chief Operating Officer (COO)', 'Human Resources Manager', 'Marketing Director', 'Sales Manager', 'IT Project Manager', 'Software Engineer', 'Data Analyst', 'Graphic Designer', 'Customer Service Representative', 'Account Manager', 'Financial Analyst', 'Operations Manager', 'Content Writer', 'Product Manager', 'Business Development Manager', 'Research Scientist', 'Quality Assurance Engineer', 'Social Media Manager', 'Procurement Specialist', 'Web Developer', 'Systems Administrator', 'HR Generalist', 'Sales Associate', 'IT Support Specialist', 'Event Coordinator', 'Project Coordinator', 'Financial Controller', 'Marketing Coordinator', 'Public Relations Specialist', 'UX/UI Designer', 'Database Administrator', 'Supply Chain Manager', 'Operations Analyst', 'Copywriter', 'Accountant', 'Investment Analyst', 'Logistics Coordinator', 'Customer Success Manager', 'Business Analyst', 'Technical Support Engineer', 'Digital Marketing Specialist', 'Network Engineer', 'Recruitment Specialist', 'Brand Manager', 'Market Research Analyst', 'Software Developer', 'Operations Supervisor', 'Administrative Assistant', 'Data Scientist', 'Sales Representative', 'Project Manager', 'IT Manager', 'Content Manager', 'Financial Planner', 'Operations Coordinator', 'Social Media Specialist', 'Procurement Manager', 'Web Designer', 'Systems Analyst', 'HR Assistant', 'Marketing Assistant', 'Customer Support Specialist', 'Event Planner', 'Business Development Representative', 'Research Analyst', 'Quality Control Inspector', 'SEO Specialist', 'Network Administrator', 'Inventory Manager', 'Data Entry Clerk', 'Executive Assistant', 'Public Relations Manager', 'Database Analyst', 'Software Architect', 'Operations Director', 'Marketing Manager', 'IT Director', 'Human Resources Director', 'Customer Service Manager', 'Quality Assurance Analyst', 'Digital Marketing Manager', 'Brand Ambassador', 'Sales Director', 'Content Strategist', 'Data Engineer', 'Systems Engineer', 'Market Research Manager', 'Supply Chain Analyst', 'Event Manager', 'Product Marketing Manager', 'Business Operations Manager', 'IT Support Manager', 'Social Media Coordinator', 'Public Relations Coordinator', 'Customer Success Coordinator', 'HR Coordinator', 'E-commerce Manager', 'Front End Developer', 'Back End Developer', 'UX/UI Architect', 'Product Owner', 'Logistics Manager', 'Marketing Specialist', 'Network Technician', 'Systems Support Specialist', 'Business Development Executive', 'Data Entry Specialist', 'Sales Analyst', 'Content Editor', 'Account Executive', 'IT Consultant', 'HR Manager', 'Marketing Analyst', 'Customer Support Representative', 'SEO Analyst', 'Sales Operations Manager', 'Content Creator', 'Financial Operations Analyst', 'Database Developer', 'Software Tester', 'Business Intelligence Analyst', 'IT Project Coordinator', 'Customer Relationship Manager', 'Quality Assurance Manager', 'CustCustomer Support Specialist']
person_titles = ['Chief Marketing Officer', 'Chief Technology Officer', 'Chief Strategy Officer', 'Chief Innovation Officer', 'Chief Data Officer', 'Chief Analytics Officer', 'Chief Information Officer', 'Chief Security Officer', 'Chief Privacy Officer', 'Chief Risk Officer', 'Chief Compliance Officer', 'Chief Legal Officer', 'Chief People Officer', 'Chief Talent Officer', 'Chief Learning Officer', 'Chief Culture Officer', 'Chief Diversity Officer', 'Chief Communications Officer', 'Chief Brand Officer', 'Chief Creative Officer', 'Chief Experience Officer', 'Chief Product Officer', 'Chief Operations Officer', 'Chief Supply Chain Officer', 'Chief Procurement Officer', 'Chief Logistics Officer', 'Chief Quality Officer', 'Chief Project Officer', 'Chief Revenue Officer', 'Chief Growth Officer', 'Chief Partnership Officer', 'Chief Customer Officer', 'Chief Client Officer', 'Chief Sales Officer', 'Chief Service Officer', 'Chief Support Officer', 'Chief Relationship Officer', 'Chief Financial Strategist', 'Director of Human Resources', 'Human Resources Business Partner', 'Talent Acquisition Manager', 'Compensation and Benefits Manager', 'Learning and Development Manager', 'Employee Relations Manager', 'Organizational Development Manager', 'Workforce Planning Manager', 'Recruitment Manager', 'Training Manager', 'Employee Engagement Specialist', 'Employment Branding Specialist', 'Workplace Wellness Coordinator', 'Diversity and Inclusion Manager', 'Internal Communications Manager', 'Employee Success Manager', 'Learning Experience Designer', 'Change Management Consultant', 'Marketing Strategist', 'Digital Marketing Manager', 'Content Marketing Specialist', 'Brand Strategist', 'Social Media Strategist', 'Public Relations Manager', 'Advertising Manager', 'Market Research Manager', 'Product Development Manager', 'Marketing Analytics Manager', 'Sales Operations Manager', 'Business Development Executive', 'Partnership Manager', 'Channel Sales Manager', 'Key Account Manager', 'Sales Enablement Specialist', 'Salesforce Administrator', 'CRM Manager', 'Technical Account Manager', 'Customer Success Manager', 'Client Relationship Manager', 'Client Services Manager', 'Customer Experience Manager', 'Customer Support Manager', 'Customer Retention Specialist', 'Customer Insights Analyst', 'Customer Journey Analyst', 'Business Analyst', 'Financial Analyst', 'Data Analyst', 'Market Analyst', 'Operations Analyst', 'Supply Chain Analyst', 'Business Intelligence Analyst', 'Risk Analyst', 'Investment Analyst', 'Quantitative Analyst', 'Compliance Analyst', 'IT Project Manager', 'Software Development Manager', 'Systems Architect', 'Data Engineer', 'Database Administrator', 'Network Administrator', 'IT Security Specialist', 'Cloud Solutions Architect', 'Infrastructure Manager', 'Technical Support Manager', 'Quality Assurance Manager', 'UX/UI Designer', 'Product Manager', 'Agile Coach', 'Scrum Master', 'Process Improvement Specialist', 'Operations Manager', 'Logistics Manager', 'Procurement Manager', 'Warehouse Manager', 'Inventory Control Manager', 'Quality Control Manager', 'Production Supervisor', 'Manufacturing Engineer', 'Supply Chain Planner', 'Operations Research Analyst', 'Environmental Health and Safety Manager', 'Content Writer', 'Editorial Manager', 'Creative Director', 'Web Designer', 'Graphic Artist', 'Multimedia Specialist', 'Video Production Manager', 'User Experience Researcher', 'User Interface Developer', 'Front End Developer', 'Back End Developer', 'Mobile App Developer', 'Data Scientist', 'Machine Learning Engineer', 'Artificial Intelligence Specialist', 'Robotics Engineer', 'Cybersecurity Analyst', 'Information Security Manager', 'IT Audit Manager', 'Project Manager', 'Program Manager', 'Operations Director', 'Marketing Manager', 'Sales Manager', 'IT Manager', 'Human Resources Director', 'Customer Service Manager', 'Quality Assurance Analyst', 'E-commerce Manager', 'Business Operations Manager', 'Social Media Coordinator', 'Customer Success Coordinator', 'HR Coordinator', 'Marketing Coordinator', 'Operations Coordinator', 'Procurement Specialist', 'Web Developer', 'Systems Analyst', 'HR Assistant', 'Sales Associate', 'IT Support Specialist', 'Event Coordinator', 'Project Coordinator', 'Financial Controller', 'Public Relations Specialist', 'Supply Chain Manager', 'Copywriter', 'Accountant', 'Logistics Coordinator', 'Technical Support Engineer', 'Digital Marketing Specialist', 'Network Engineer', 'Recruitment Specialist', 'Brand Manager', 'Market Research Analyst', 'Software Developer', 'Operations Supervisor', 'Administrative Assistant', 'Sales Representative', 'Content Manager', 'Financial Planner', 'Social Media Specialist', 'Marketing Assistant', 'Customer Support Specialist', 'Event Planner', 'Business Development Representative', 'Research Analyst', 'Quality Control Inspector', 'SEO Specialist', 'Inventory Manager', 'Data Entry Clerk', 'Executive Assistant', 'Database Analyst', 'Software Architect', 'IT Director', 'Brand Ambassador', 'Sales Director', 'Content Strategist', 'Systems Engineer', 'Event Manager', 'Product Marketing Manager', 'IT Support Manager', 'Public Relations Coordinator', 'UX/UI Architect', 'Product Owner', 'Marketing Specialist', 'Network Technician', 'Systems Support Specialist', 'Data Entry Specialist', 'Sales Analyst', 'Content Editor', 'Account Executive', 'IT Consultant', 'HR Manager', 'Marketing Analyst', 'Customer Support Representative', 'SEO Analyst', 'Content Creator', 'Financial Operations Analyst', 'Database Developer', 'Software Tester', 'IT Project Coordinator', 'Customer Relationship Manager']


# api_key = "LYnrNuerHa1JM7jtirPAdQ"
api_key = "RpmpggrZQW-Jolqs2F5xCw"

per_page = 50

headers = {
    "Content-Type": "application/json",
    "Cache-Control": "no-cache"
}

all_people = []
needed_data = int(input("Enter the number of data needed: "))
data_count = 0

def get_proxy():
    proxy_list = scrape_proxy_list()
    working_proxy = None

    for proxy in proxy_list:
        if test_proxy(proxy):
            working_proxy = proxy
            break
    proxies = {'http': working_proxy, 'https': working_proxy}
    return proxies

# proxies = get_proxy()
# print(proxies)

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
            # proxies = get_proxy()
            # print(proxies)
            print(f"Error: Request failed for '{person_title}' with status code {response.status_code}")
            page += 1
            break

flattened_people = [flatten(person) for person in all_people]

field_names = set().union(*[person.keys() for person in flattened_people])

with open(csv_file, 'w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=field_names)
    writer.writeheader()
    writer.writerows(flattened_people)

