# from _typeshed import Self
from typing import Any, List
from bs4 import BeautifulSoup
import requests
from requests.models import Response
import re
import os
import csv
from pathlib import Path


def save_country_result_data(path: str, data, header):
    splitted = path.split('/')
    path = '/'.join(splitted[:-1])
    
    folder = Path(path)
    folder.mkdir(parents=True, exist_ok=True)

    with open(str(folder / splitted[-1]) , 'w+', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(data)


floatOrZero = lambda x : 0 if x is None else float(x)

def parseTime(str):        
        m = re.match(r"((?P<min>\d+):)?(?P<seg>\d+)(\.(?P<ms>\d+).*)?", str)
        if m is None :
            return None
        else:
            r = floatOrZero(m.groupdict()['min'])*60 + \
                floatOrZero(m.groupdict()['seg']) + \
                floatOrZero(m.groupdict()['ms'])/100
            return r

# print(parseTime("2:59.30"))
# print(parseTime("10.07"))

def getLetters(imageLink: str):
    m = re.search(r"\w{3}(?=.gif)", imageLink)

    if m is None:
        return None
    return m.group(0)


class EventResultCountryScrapper():

    def __init__(self, event_name):
        self.event_name = event_name

    @staticmethod
    def __get_row_data(row: BeautifulSoup, data: str, cast_type: type = None):
        extracted = row.find('td', {'data-th': data}).text.strip()
        if cast_type is not None:
            try:
                cast_type(extracted)
            except ValueError:
                return parseTime(extracted)
        return extracted
    
    def default_scraper(self, rows: List[BeautifulSoup]) -> List[Any]:
        data = []
        for row in rows[1:]:
            # mark = row.find('td', {'data-th': 'Mark'})

            mark = self.__get_row_data(row, 'Mark')
            country = self.__get_row_data(row, 'Nat')

            floatMark = parseTime(mark)

            # _imageLink = country.find('img').attrs['src']
            # countryLetters = getLetters(_imageLink)

            data.append([country, floatMark]) # YEARRRR
        return data

    def scrap(self, html: BeautifulSoup) -> List[Any]:
        table: BeautifulSoup = html.find('table', class_='records-table')
        rows: BeautifulSoup = table.find_all('tr')
    
        return self.default_scraper(rows)

resultsDict = {
    'atl_4x100m':{
        'female': {},
        'male': {}
    },
    'atl_4x400m':{
        'female': {},
        'male': {},
        'mixed': {}
    }
}

class CountryScrapper():

    def __init__(self) -> None:
        pass

    def __results_request(self, year, event_name, gender) -> Response:
        base_url = 'https://www.worldathletics.org/records/toplists/relays/'
        tail = '?regionType=world&timing=electronic&page=1&bestResultsOnly=true'
        url = base_url + event_name + '/outdoor/' + gender + '/senior/' + str(year) + tail
        return requests.get(url)
    
    
    def save_event_results_offline(self, file_path: str): # like: 'htmls/relays/4x100m_F_2018.html'
        event_name, gender, year = file_path.split('/')[-1].split('.')[0].split('_')
        event_name = 'atl_' + event_name
        gender = 'female' if gender == 'F' else ('male' if gender == 'M' else 'mixed')

        with open(file_path, 'r', encoding='utf-8') as html:
        # Building soup
            soup = BeautifulSoup(html, 'lxml')

            # Building profile data scrapper
            ercs = EventResultCountryScrapper(event_name)
            scrap = ercs.scrap(soup)

        if scrap is None:                
            print(f'\t\tCould not scrap year {year}')

        # resultsDict = {} # Country -> (year, result)
        for country, mark in scrap:
            if country not in resultsDict[event_name][gender]:
                resultsDict[event_name][gender][country] = []
            resultsDict[event_name][gender][country].append((year, mark))


        # for country in resultsDict:
        #     header = ['Date', 'Result']
        #     result_file_path = '/'.join(['classified', event_name, gender, country + '.csv'])
        #     save_country_result_data(result_file_path, resultsDict[country], header)
        
        # return resultsDict

    def get_event_results(self, event: str, gender, years: List[int],
                          logs: bool = True):
        if logs:
            print(f'Scrapping. Event {event}')

        data = []
        for year in years:
            if logs:
                print(f'\tYear: {year}')

            # resp: Response = self.__results_request(year, event, gender)
            # if resp.status_code != 200:
            #     print(f'Could not scrap year {year}. Status code: {resp.status_code}')
            #     continue

            # html = str(resp.content, encoding=resp.encoding)

            with open('htmls/relays/4x100m_F_2018.html', 'r', encoding='utf-8') as html:
            # Building soup
                soup = BeautifulSoup(html, 'lxml')

                # Building profile data scrapper
                ercs = EventResultCountryScrapper(event)
                scrap = ercs.scrap(soup)

            if scrap is None:                
                print(f'\t\tCould not scrap year {year}')
                continue

            scrap = [(c, year, r) for c, r in scrap]
            data.extend(scrap)

        resultsDict = {} # Country -> (year, result)
        for country, year, mark in scrap:
            if country not in resultsDict:
                resultsDict[country] = []
            resultsDict[country].append((year, mark))

        return resultsDict

country_sc = CountryScrapper()
# print(country_sc.get_event_results('4x100 Metres Relay 2021', 'women', [2018]))

for root, dirs, files in os.walk('htmls/relays'):
    for file in files:
        file_name = '/'.join([root, file])
        country_sc.save_event_results_offline(file_name)

for event, data in resultsDict.items():
    for sex, countries in data.items():
        for country in countries:
            header = ['Date', 'Result']
            result_file_path = '/'.join(['classified', event, sex, country + '.csv'])
            save_country_result_data(result_file_path, resultsDict[event][sex][country], header)
