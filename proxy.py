import requests
from bs4 import BeautifulSoup

def test_proxy(proxy):
    url = 'https://www.example.com'
    proxies = {'http': proxy, 'https': proxy}
    
    try:
        response = requests.get(url, proxies=proxies, timeout=5)
        if response.status_code == 200:
            return True
    except:
        pass
    
    return False

def scrape_proxy_list():
    url = 'https://www.free-proxy-list.net/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    proxy_list = []
    table = soup.find('table')
    
    if table is not None:
        rows = table.find_all('tr')
        for row in rows[1:]:
            columns = row.find_all('td')
            ip = columns[0].text
            port = columns[1].text
            proxy = f'{ip}:{port}'
            proxy_list.append(proxy)
    
    return proxy_list

# proxies = scrape_proxy_list()
# working_proxy = None

# for proxy in proxies:
#     if test_proxy(proxy):
#         working_proxy = proxy
#         break

# if working_proxy is not None:
#     print("Working proxy found:", working_proxy)
# else:
#     print("No working proxies found.")
