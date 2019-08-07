import requests
from bs4 import BeautifulSoup
import json
import re

url = 'https://www.reddit.com/r/gameofthrones/wiki/episode_discussion'
headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}


def extract_data_from_table(table_elem):
    try:
        episode_title = table_elem.find_previous("h4").text

        # use regex pattern matching to extract season and episode from the title
        title_patt = r'(\d+)\.(\d+)\s(.*)'
        title_match = re.search(title_patt, episode_title)
        season = title_match.group(1)
        episode = title_match.group(2)
        title = title_match.group(3)

        # use css selectors to get reddit submission and youtube link
        links = table_elem.select("td a")
        links_dict = {}
        for link in links:
            links_dict[link.text] = link['href']
    except:
        print("problem with table {}".format(table_elem))

    return {
        'season': season,
        'episode': episode,
        'title': title,
        'links' : links_dict
    }


if __name__ == '__main__':
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text)
    # find all the table elements in the html
    tables = soup.find_all("table")

    records = []
    for table in tables:
        records.append(extract_data_from_table(table))

    with open('got_reddit_links.json', 'w') as got_links:
        json.dump(records, got_links, indent=2)
