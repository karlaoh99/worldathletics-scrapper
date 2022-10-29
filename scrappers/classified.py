from bs4 import BeautifulSoup
from .url import URL
import requests
from pathlib import Path
import urllib.request
from selenium import webdriver
import time
import re
import json

W_100M = "Women's 100m"
W_200M = "Women's 200m"
W_400M = "Women's 400m"
W_800M = "Women's 800m"
W_1500M = "Women's 1500m"
W_5000M = "Women's 5000m"
W_10000M = "Women's 10,000m"
W_100MH = "Women's 100mH"
W_400MH = "Women's 400mH"
W_3000MSC = "Women's 3000mSC"
W_HIGH_JUMP = "Women's High Jump"
W_POLE_VAULT = "Women's Pole Vault"
W_LONG_JUMP = "Women's Long Jump"
W_TRIPLE_JUMP = "Women's Triple Jump"
W_SHOT_PUT = "Women's Shot Put"
W_DISCUS_THROW = "Women's Discus Throw"
W_HAMMER_THROW = "Women's Hammer Throw"
W_JAVELIN_THROW = "Women's Javelin Throw"
W_MARATHON = "Women's Marathon"
W_20KM_RACE_WALK = "Women's 20km Race Walk"
W_50KM_RACE_WALK = "Women's 50km Race Walk"
W_HEPTATHLON = "Women's Heptathlon"
W_4X100M = "Women's 4x100m"
W_4X400M = "Women's 4x400m"
M_100M = "Men's 100m"
M_200M = "Men's 200m"
M_400M = "Men's 400m"
M_800M = "Men's 800m"
M_1500M = "Men's 1500m"
M_5000M = "Men's 5000m"
M_10000M = "Men's 10,000m"
M_110MH = "Men's 110mH"
M_400MH = "Men's 400mH"
M_3000MSC = "Men's 3000mSC"
M_HIGH_JUMP = "Men's High Jump"
M_POLE_VAULT = "Men's Pole Vault"
M_LONG_JUMP = "Men's Long Jump"
M_TRIPLE_JUMP = "Men's Triple Jump"
M_SHOT_PUT = "Men's Shot Put"
M_DISCUS_THROW = "Men's Discus Throw"
M_HAMMER_THROW = "Men's Hammer Throw"
M_JAVELIN_THROW = "Men's Javelin Throw"
M_MARATHON = "Men's Marathon"
M_20KM_RACE_WALK = "Men's 20km Race Walk"
M_50KM_RACE_WALK = "Men's 50km Race Walk"
M_DECATHLON = "Men's Decathlon"
M_4X100M = "Men's 4x100m"
M_4X400M = "Men's 4x400m"
MIX_4X400M = "Mixed 4x400m"

event_name = {
    ('atl_100m', 'female'): W_100M,
    ('atl_200m', 'female'): W_200M,
    ('atl_400m', 'female'): W_400M,
    ('atl_800m', 'female'): W_800M,
    ('atl_1500m', 'female'): W_1500M,
    ('atl_5000m', 'female'): W_5000M,
    ('atl_10000m', 'female'): W_10000M,
    ('atl_100v', 'female'): W_100MH,
    ('atl_400v', 'female'): W_400MH,
    ('atl_3000m', 'female'): W_3000MSC,
    ('atl_alt', 'female'): W_HIGH_JUMP,
    ('atl_per', 'female'): W_POLE_VAULT,
    ('atl_lar', 'female'): W_LONG_JUMP,
    ('atl_tri', 'female'): W_TRIPLE_JUMP,
    ('atl_bal', 'female'): W_SHOT_PUT,
    ('atl_dis', 'female'): W_DISCUS_THROW,
    ('atl_mar', 'female'): W_HAMMER_THROW,
    ('atl_jab', 'female'): W_JAVELIN_THROW,
    ('atl_mat', 'female'): W_MARATHON,
    ('atl_20km', 'female'): W_20KM_RACE_WALK,
    ('atl_50km', 'female'): W_50KM_RACE_WALK,
    ('atl_hep', 'female'): W_HEPTATHLON,
    ('atl_4x100m', 'female'): W_4X100M,
    ('atl_4x400m', 'female'): W_4X400M,
    ('atl_100m', 'male'): M_100M,
    ('atl_200m', 'male'): M_200M,
    ('atl_400m', 'male'): M_400M,
    ('atl_800m', 'male'): M_800M,
    ('atl_1500m', 'male'): M_1500M,
    ('atl_5000m', 'male'): M_5000M,
    ('atl_10000m', 'male'): M_10000M,
    ('atl_110v', 'male'): M_110MH,
    ('atl_400v', 'male'): M_400MH,
    ('atl_3000m', 'male'): M_3000MSC,
    ('atl_alt', 'male'): M_HIGH_JUMP,
    ('atl_per', 'male'): M_POLE_VAULT,
    ('atl_lar', 'male'): M_LONG_JUMP,
    ('atl_tri', 'male'): M_TRIPLE_JUMP,
    ('atl_bal', 'male'): M_SHOT_PUT,
    ('atl_dis', 'male'): M_DISCUS_THROW,
    ('atl_mar', 'male'): M_HAMMER_THROW,
    ('atl_jab', 'male'): M_JAVELIN_THROW,
    ('atl_mat', 'male'): M_MARATHON,
    ('atl_20km', 'male'): M_20KM_RACE_WALK,
    ('atl_50km', 'male'): M_50KM_RACE_WALK,
    ('atl_dec', 'male'): M_DECATHLON,
    ('atl_4x100m', 'male'): M_4X100M,
    ('atl_4x400m', 'male'): M_4X400M,
    ('atl_4x400m', 'mixed'): MIX_4X400M
}

event_id = {
    W_100M: '10229509',
    W_200M: '10229510',
    W_400M: '10229511',
    W_800M: '10229512',
    W_1500M: '10229513',
    W_5000M: '10229514',
    W_10000M: '10229521',
    W_100MH: '10229522',
    W_400MH: '10229523',
    W_3000MSC: '10229524',
    W_HIGH_JUMP: '10229526',
    W_POLE_VAULT: '10229527',
    W_LONG_JUMP: '10229528',
    W_TRIPLE_JUMP: '10229529',
    W_SHOT_PUT: '10229530',
    W_DISCUS_THROW: '10229531',
    W_HAMMER_THROW: '10229532',
    W_JAVELIN_THROW: '10229533',
    W_MARATHON: '10229534',
    W_20KM_RACE_WALK: '10229535',
    W_50KM_RACE_WALK: '10229603',
    W_HEPTATHLON: '10229536',
    W_4X100M: '204594',
    W_4X400M: '204596',
    M_100M: '10229630',
    M_200M: '10229605',
    M_400M: '10229631',
    M_800M: '10229501',
    M_1500M: '10229502',
    M_5000M: '10229609',
    M_10000M: '10229610',
    M_110MH: '10229611',
    M_400MH: '10229612',
    M_3000MSC: '10229614',
    M_HIGH_JUMP: '10229615',
    M_POLE_VAULT: '10229616',
    M_LONG_JUMP: '10229617',
    M_TRIPLE_JUMP: '10229618',
    M_SHOT_PUT: '10229619',
    M_DISCUS_THROW: '10229620',
    M_HAMMER_THROW: '10229621',
    M_JAVELIN_THROW: '10229636',
    M_MARATHON: '10229634',
    M_20KM_RACE_WALK: '10229508',
    M_50KM_RACE_WALK: '10229628',
    M_DECATHLON: '10229629',
    M_4X100M: '204593',
    M_4X400M: '204595',
    MIX_4X400M: '10229988'
}

event_profile_name = {
    W_100M: '100 Metres',
    W_200M: '200 Metres',
    W_400M: '400 Metres',
    W_800M: '800 Metres',
    W_1500M: '1500 Metres',
    W_5000M: '5000 Metres',
    W_10000M: '10,000 Metres',
    W_100MH: '100 Metres Hurdles',
    W_400MH: '400 Metres Hurdles',
    W_3000MSC: '3000 Metres Steeplechase',
    W_HIGH_JUMP: 'High Jump',
    W_POLE_VAULT: 'Pole Vault',
    W_LONG_JUMP: 'Long Jump',
    W_TRIPLE_JUMP: 'Triple Jump',
    W_SHOT_PUT: 'Shot Put',
    W_DISCUS_THROW: 'Discus Throw',
    W_HAMMER_THROW: 'Hammer Throw',
    W_JAVELIN_THROW: 'Javelin Throw',
    W_MARATHON: 'Marathon',
    W_20KM_RACE_WALK: '20 Kilometres Race Walk',
    W_50KM_RACE_WALK: '50 Kilometres Race Walk',
    W_HEPTATHLON: 'Heptathlon',
    W_4X100M: '-',
    W_4X400M: '-',
    M_100M: '100 Metres',
    M_200M: '200 Metres',
    M_400M: '400 Metres',
    M_800M: '800 Metres',
    M_1500M: '1500 Metres',
    M_5000M: '5000 Metres',
    M_10000M: '10,000 Metres',
    M_110MH: '110 Metres Hurdles',
    M_400MH: '400 Metres Hurdles',
    M_3000MSC: '3000 Metres Steeplechase',
    M_HIGH_JUMP: 'High Jump',
    M_POLE_VAULT: 'Pole Vault',
    M_LONG_JUMP: 'Long Jump',
    M_TRIPLE_JUMP: 'Triple Jump',
    M_SHOT_PUT: 'Shot Put',
    M_DISCUS_THROW: 'Discus Throw',
    M_HAMMER_THROW: 'Hammer Throw',
    M_JAVELIN_THROW: 'Javelin Throw',
    M_MARATHON: 'Marathon',
    M_20KM_RACE_WALK: '20 Kilometres Race Walk',
    M_50KM_RACE_WALK: '50 Kilometres Race Walk',
    M_DECATHLON: 'Decathlon',
    M_4X100M: '-',
    M_4X400M: '-',
    MIX_4X400M: '-'
}

# ROAD TO OREGON
BASE_URL = URL('https://worldathletics.org/stats-zone/road-to/7125365')


athletes_urls = {}


class ClassifiedCountries():

    def __scrap_row(self, row: BeautifulSoup):
        country_class = 'QualifiedCompetitors_countryWidth__2x3gQ'
        country = row.find('td', class_=country_class).text
        return country

    def scrap_html(self, html: str, athletes_count=40):
        # Building soup
        soup = BeautifulSoup(html, 'lxml')

        container: BeautifulSoup = soup.find('table')
        rows = container.find_all('tr')
        rows.pop(0)
        rows = rows[:athletes_count]

        return [[self.__scrap_row(r)] for r in rows]


class ClassifiedAthletes():

    def __init__(self, event_name: str):
        self.event_name = event_name
        self.url = BASE_URL.add_param('eventId', event_id[event_name])
        self.time = 3
        print(self.url)
    
    def get_athlete_url_profile(sefl, athlete_name):
        saved_url = athletes_urls.get(athlete_name, None)

        if saved_url is not None:
            print("*** athlete url found on cache ***")
            return saved_url

        url = 'https://www.worldathletics.org/athletes/search?query='
        url += '%20'.join(athlete_name.split())
        print(f'    Searching for {athlete_name}')
        resp = requests.get(url)
        html = str(resp.content, encoding=resp.encoding)

        patt = r'\"urlSlug\":\"(.*?)\"'
        match = re.search(patt, html)
        link = match.group(1)
        print(f'    Found: {link}')
        full_url = 'https://www.worldathletics.org/athletes/' + link
        athletes_urls[athlete_name] = full_url
        return full_url

    def __scrap_athlete(self, row: BeautifulSoup) -> str:
        a_tag = row.find('a')
        country_class = 'QualifiedCompetitors_countryWidth__2x3gQ'
        country = row.find('td', class_=country_class).text
        return (a_tag.text, country, a_tag['href'])
    
    def __scrap_athlete_clickable(self, row: BeautifulSoup) -> str:
        athlete_name = row.find('div').text
        link = self.get_athlete_url_profile(athlete_name)
        country_class = 'QualifiedCompetitors_countryWidth__2x3gQ'
        country = row.find('td', class_=country_class).text
        return (athlete_name, country, link)
    
    def scrap_html(self, html: str, athletes_count=40):
        # Building soup
        soup = BeautifulSoup(html, 'lxml')

        container: BeautifulSoup = soup.find('table')
        rows = container.find_all('tr')
        rows.pop(0)
        rows = rows[:athletes_count]

        click_pointer_class = 'QualifiedCompetitors_rowClickPointer__1itql'
        non_click_rows = [r for r in rows if click_pointer_class not in r.attrs['class']]
        click_rows = [r for r in rows if r not in non_click_rows]

        urls_1 = [self.__scrap_athlete(r) for r in non_click_rows]
        urls_2 = [self.__scrap_athlete_clickable(r) for r in click_rows]
        return urls_1 + urls_2
    
    def download_classification_html(self, browser: webdriver.Firefox, event: str, sex: str, path: str):
        full_path = Path(path)
        full_path.mkdir(parents=True, exist_ok=True)
        full_path /= f'{event}-{sex}.html'
        # if full_path.exists():
        #     return
        print('Loading page...')
        try:
            browser.get(str(self.url))
            i = 1
            html = browser.page_source
            while 'table cellspacing' not in html:
                if self.time != 0:
                    print(f'Time {i}s...')
                time.sleep(1)
                i += 1
                html = browser.page_source
            print(f'Saving {event} {sex} ...')
            with open(str(full_path), 'w+', encoding='utf-8') as f:
                f.write(html)
        except Exception as e:
            print(f'[ERROR] {e}')
            pass
    
    # def get_first_athletes_urls(self, html: str, athletes_count=40):
    #     return self.scrap_html(html, athletes_count)
