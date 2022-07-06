from scrappers import AthleteScrapper
import scrappers.classified as clasf
import csv
from pathlib import Path
from selenium import webdriver
from concurrent.futures import *


years = [2022, 2021, 2020]


def save_world_ranking_data(path: str, data):
    with open(path, 'w+', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        header = ['rank', 'name', 'dob', 'nat', 'score', 'performance_file_name']
        writer.writerow(header)
        writer.writerows(data)


def save_athlete_result_data(path: str, data, header):
    with open(path, 'w+', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(data)


def scrap_relays(folder_path: str, event_name: str, html, athletes_count: int = 250):
    cl_scrapper = clasf.ClassifiedCountries()

    countries = cl_scrapper.scrap_html(html, athletes_count)
    folder = Path(folder_path)
    folder.mkdir(parents=True, exist_ok=True)
    print('Saving classified result')
    data_file_path = folder / 'classified.csv'
    with open(str(data_file_path), 'w+', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(countries)


def scrap_classified(folder_path: str, event_name: str, html, total_percent, athletes_count: int = 40):
    if 'x' in event_name:
        scrap_relays(folder_path, event_name, html, athletes_count)
        return

    cl_scrapper = clasf.ClassifiedAthletes(event_name)

    athletes_urls = cl_scrapper.scrap_html(html, athletes_count)
    print(athletes_urls)
    i = 1
    for name, country, url in athletes_urls:
        percent = i * 100 / len(athletes_urls)
        i += 1
        print(f'Scrap progress {total_percent:.2f} %  -  Event progress {percent:.2f} %')

        file_name = country + '_' + name.lower().replace(' ', '_')
        folder = Path(folder_path)
        folder.mkdir(parents=True, exist_ok=True)
        print('Saving classified athlete result')
        data_file_path = folder / f'{file_name}.csv'
        # if data_file_path.exists():
        #     print(f'Already exist data for athlete {name}')
        #     continue

        event = clasf.event_profile_name[event_name]
        ath_scrapper = AthleteScrapper(url)
        results = ath_scrapper.get_event_results(event=event, years=years)
        event += ' Indoor'
        results += ath_scrapper.get_event_results(event=event, years=years)
        header = ['Date', 'Result']
        save_athlete_result_data(str(data_file_path), results, header)


def scrap_clasf_event(tup, name, percent):
    event, sex = tup
    # if 'x' not in event:
    #     return
    html = None
    with open(f'htmls/{event}-{sex}.html', 'r', encoding='utf-8') as f:
        html = f.read()
    scrap_classified(f'classified/{event}/{sex}/', name, html, percent, 250)


# Download htmls
def download_classification_htmls():
    browser = webdriver.Firefox()
    path = 'htmls/'
    for tup, name in clasf.event_name.items():
        event, sex = tup
        cl = clasf.ClassifiedAthletes(name)
        cl.download_classification_html(browser, event, sex, path)
    browser.close()


def main():
    download_classification_htmls()

    i, total = 1, len(clasf.event_name.items())
    for tup, name in clasf.event_name.items():
        percent = i * 100 / total
        scrap_clasf_event(tup, name, percent)
    i += 1


if __name__ == '__main__':
    # proxecutor = ThreadPoolExecutor()
    # tasks = [proxecutor.submit(scrap_clasf_event, tup, name, 0) for tup, name in clasf.event_name.items()]
    # wait(tasks, return_when=ALL_COMPLETED)
    main()