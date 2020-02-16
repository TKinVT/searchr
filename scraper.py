import os
import string
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
load_dotenv()

BASE_URL = os.getenv("TORRENT_SITE_URL")


def clean_search_term(search_term):
    cleaner = ""
    for char in search_term:
        if char in string.ascii_letters or char in string.digits \
        or char in string.whitespace or char == '"':
            cleaner += char
    new_term = cleaner.replace(' ', '%20')
    return new_term

def search_matey(search_term, search_type, num_results=5):

    # adapted switch statement solution from stackoverflow suggestions
    # https://stackoverflow.com/questions/60208/replacements-for-switch-statement-in-python
    search_types = {
        'movie': '200',
        'tv': '200',
        'audio': '100',
        'audiobook': '600',
        'other': '0',
        None: '0'
    }

    result_types = {
        'Movies': 'movie',
        'HD - Movies': 'movie',
        'Music videos': 'musicvideo',
        'TV Shows': 'tv',
        'Music': 'audio',
        'FLAC': 'audio',
        'Audio books': 'audiobook'
    }

    search_type = search_types[search_type]
    search_term = clean_search_term(search_term)
    url = BASE_URL + "/search/{}/0/99/".format(search_term) + search_type
    doc = requests.get(url).text
    soup = BeautifulSoup(doc, 'html.parser')

    table = soup.table
    rows = table.find_all('tr')
    header = rows.pop(0).find_all('th')
    header_cols = [x.a.text for x in header]

    results = []
    for row in rows[:num_results]:
        row_cells = row.find_all('td')
        row_type = row_cells[0].find_all('a')[1].text
        if row_type in result_types:
            row_type = result_types[row_type]
        row_name = row_cells[1].a.text
        row_magnet_link = row_cells[1].find_all('a')[1]['href']
        row_seeders = row_cells[2].text
        row_leechers = row_cells[3].text
        result = {"type": row_type, "name": row_name, "seeders": row_seeders,
                  "leechers": row_leechers, "magnet_link": row_magnet_link}
        results.append(result)

    return results

if __name__ == '__main__':
    import sys
    search = sys.argv[1]
    s = search_matey(search, None)
    print(s)
    # print("SE\t|LE\t|Name")
    # print("--\t --\t --")
    # for result in s:
    #     print("{}\t|{}\t|{}\n{}".format(result['seeders'], result['leechers'], result['name'],result['magnet_link']))
