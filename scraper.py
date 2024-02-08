import pandas as pd
from cloudscraper import create_scraper
from bs4 import BeautifulSoup
import concurrent.futures
from time import sleep

BASE_URL = 'https://cedia2023.smallworldlabs.com/exhibitors/exhibitor'

with open('id.txt', 'r') as f:
    id_list = f.readlines()
    id_list = [x.replace('\n', '') for x in id_list]

s = create_scraper()

def get_data(link):   
    resp = s.get(link)
    soup = BeautifulSoup(resp.text, 'lxml')
    try:
        booth = soup.select_one('.fas.fa-map-marker-alt').next
    except:
        booth = None
    try:
        name = soup.select_one('.profileResponse').text
    except:
        name = None
    try:
        website = soup.select_one('.profileResponse a')['href']
    except:
        website = None
    item = {
        'Booth': booth,
        'Name': name,
        'Website': website
    }
    exhibitors.append(item)
    print(link)
    print(item)
    sleep(3)

if __name__ == '__main__':
    exhibitors = []
    links = []
    n = 0
    for x in id_list:
        link = f'{BASE_URL}/{x}'
        links.append(link)

    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(get_data, links)

    df = pd.DataFrame(exhibitors)
    df.to_excel('cedia_exhibitors.xlsx', index=False)