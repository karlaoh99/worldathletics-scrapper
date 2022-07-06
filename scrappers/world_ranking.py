from .url import URL
from bs4 import BeautifulSoup
import requests

BASE_URL = URL('https://www.worldathletics.org')

# Genders
MALE_GENDER = 'men'
FEMALE_GENDER = 'women'

# Event groups
EG_100M = '100m'
EG_DISCUS_THROW = 'discus-throw'

# Region types
RT_WORLD = 'world'

class WorldRankingScrapper():

    def __init__(self, gender: str, event_group: str) -> None:
        additional_path = f'/world-rankings/{event_group}/{gender}'
        self.__url = BASE_URL + additional_path

    @property
    def url(self):
        return self.__url

    def __request_page(self, page: int = 1):
        url = self.url.add_param('page', page)
        return requests.get(str(url))
    
    @staticmethod
    def __get_row_data(row: BeautifulSoup, data: str, cast_type: type = None): 
        extracted = row.find('td', {'data-th':data}).text.strip()
        if cast_type is not None:
            return cast_type(extracted)
        return extracted
    
    def __get_competitor_profile_link(self, row: BeautifulSoup):
        return BASE_URL.url + row.get('data-athlete-url')
    
    def __get_rows(self, page: int = 1, logs: bool = True) -> BeautifulSoup:
        if logs:
            print(f'Scrapping page {page}. URL: {self.url}')

        resp = self.__request_page(page)
        html = str(resp.content, encoding=resp.encoding)

        # Building soup
        soup = BeautifulSoup(html, 'lxml')
        return soup.find_all('tr', class_="table-row--hover")

    def get_page_data(self, page: int = 1, logs: bool = True):
        rows = self.__get_rows(page, logs)

        data = []
        for row in rows:
            rank = self.__get_row_data(row, 'Rank', int)
            competitor = self.__get_row_data(row, 'Competitor')
            dob = self.__get_row_data(row, 'DOB')
            nat = self.__get_row_data(row, 'Nat')
            score = self.__get_row_data(row, 'score', int)
            profile_url = self.__get_competitor_profile_link(row)
            data.append([rank, competitor, dob, nat, score, profile_url])
        return data

    def get_pages_data(self, from_page: int = 1, to_page: int = 1):
        data = []
        for i in range(from_page, to_page + 1):
            data.extend(self.get_page_data(i))
        return data

    def get_first_places(self, count: int = 40):
        current_page = 1
        data = []
        while len(data) < count:
            data.extend(self.get_page_data(current_page))
            current_page += 1
        return data[:count]
    
    def get_first_places_profile(self, count: int = 40):
        current_page = 1
        data = []
        while len(data) < count:
            rows = self.__get_rows(current_page, True)
            data = []
            for row in rows:
                name = self.__get_row_data(row, 'Competitor')
                profile_url = self.__get_competitor_profile_link(row)
                data.append([name, profile_url])
            current_page += 1
        return data[:count]

