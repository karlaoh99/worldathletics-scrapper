# from _typeshed import Self
from typing import Any, List
from bs4 import BeautifulSoup
import requests
from requests.models import Response
import re

floatOrZero = lambda x : 0 if x is None else float(x)

def parseTime(str):        
        m = re.match(r"((?P<hour>\d+):)?(?P<min>\d+):(?P<seg>\d+)(\.(?P<ms>\d+).*)?", str)
        if m is None :
            return None
        else:
            r = floatOrZero(m.groupdict()['hour'])*3600 + \
                floatOrZero(m.groupdict()['min'])*60 + \
                floatOrZero(m.groupdict()['seg']) + \
                floatOrZero(m.groupdict()['ms'])/100
            return r

# print(parseTime("1:23:49"))

class EventResultProfileScrapper():

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
        for row in rows:
            date = self.__get_row_data(row, 'Date')
            if date is None or 'Date' in date:
                continue
            result = self.__get_row_data(row, 'Result', float)
            data.append([date, result])
        return data

    def scrap(self, html: BeautifulSoup) -> List[Any]:
        containers: BeautifulSoup = html.find_all('div', class_='results-by-event-wrapper results-wrapper')
        e_name = self.event_name

        container = None
        for contain in containers:
            h2 = contain.find('h2')
            text = h2.text.strip()
            if text == e_name:
                container = contain
                break
        
        if container is None:
            return None
    
        table = container.find_all('tr')
    
        return self.default_scraper(table)


class AthleteScrapper():

    def __init__(self, url: str) -> None:
        self.__url = url

    @property
    def url(self):
        return self.__url
    
    @property
    def athlete_name(self):
        athlete = self.url.split('/')[-1]
        athlete = athlete.split('-')[:-1]
        return ' '.join(athlete)
    
    @property
    def athlete_id(self):
        return self.url.split('-')[-1]

    def __results_request(self, year) -> Response:
        base_url = 'https://www.worldathletics.org/data/'
        url = base_url + 'GetCompetitorResultsByYearHtml?'
        url += f'resultsByYear={year}'
        url += f'&resultsByYearOrderBy=discipline&aaId={self.athlete_id}'
        return requests.get(url)
    

    def get_event_results(self, event: str, years: List[int],
                          logs: bool = True):
        if logs:
            print(f'Scrapping. Profile: {self.athlete_name}')

        data = []
        for year in years:
            if logs:
                print(f'\tYear: {year}')

            resp: Response = self.__results_request(year)
            if resp.status_code != 200:
                print(f'Could not scrap year {year} for athlete '
                      f'{self.athlete_name}. Status code: {resp.status_code}')
                continue

            html = str(resp.content, encoding=resp.encoding)

            # Building soup        
            soup = BeautifulSoup(html, 'lxml')

            # Building profile data scrapper
            epps = EventResultProfileScrapper(event)
            scrap = epps.scrap(soup)

            if scrap is None:                
                print(f'\t\tCould not scrap year {year} for athlete '
                      f'{self.athlete_name}')
                continue

            data.extend(scrap)

        return data
