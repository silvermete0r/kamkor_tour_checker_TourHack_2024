import requests
from bs4 import BeautifulSoup
import pandas as pd

def get_counterparty_by_keyword(keyword):
    url = f"https://www.goszakup.gov.kz/ru/registry/supplierreg?filter%5Bname%5D={keyword}"
    response = requests.get(url, verify=False)
    response = response.content
    try:
        soup = BeautifulSoup(response, 'html.parser')
        tbody = soup.findAll('tbody')[2]
        data_row = tbody.find('tr')

        info = data_row.find_all('td')
        id = info[0].text.replace('\n', '').replace(' ', '').replace('\t', '').replace('\r', '')
        name = info[1].find('a').text.replace('\n', '').replace(' ', '').replace('\t', '').replace('\r', '')
        gosreestr_link = info[1].find('a')['href']
        BIN = info[2].text.replace('\n', '').replace(' ', '').replace('\t', '').replace('\r', '')
        IIN = info[3].text.replace('\n', '').replace(' ', '').replace('\t', '').replace('\r', '')

        company_info = {
            'id': id,
            'name': name,
            'gosreestr_link': gosreestr_link,
            'BIN': BIN,
            'IIN': IIN
        }

        return company_info
    except Exception as e:
        print(f'Error: {e}')
        return {
            'id': None,
            'name': None,
            'gosreestr_link': None,
            'statsnet_link': None,
            'BIN': None,
            'IIN': None
        }

tour_agents = pd.read_json('data/tour_agents_data.json', encoding='utf-8')
for index, row in tour_agents.iterrows():
    keyword = row['name']
    company_info = get_counterparty_by_keyword(keyword)
    tour_agents.at[index, 'IIN'] = company_info['IIN']
    tour_agents.at[index, 'BIN'] = company_info['BIN']
    tour_agents.at[index, 'gosreestr_link'] = company_info['gosreestr_link']
    tour_agents.at[index, 'statsnet_link'] = f'https://statsnet.co/search/kz/{keyword}'.strip().replace(' ', '%20')
    print(f'{index} / {len(tour_agents)}')

tour_agents.to_json('data/tour_agents_data.json', orient='records', indent=4)