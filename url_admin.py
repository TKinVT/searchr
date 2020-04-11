import time
import requests
import os
from dotenv import load_dotenv
from jsonbox import JsonBox


load_dotenv()
JSONBOX_ID = os.getenv("JSONBOX_ID")
API_KEY = os.getenv("API_KEY")
jb = JsonBox()


def timer(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        f = func(*args, **kwargs)
        elapsed = time.time() - start
        return [f, elapsed]
    return wrapper


@timer
def timed_get(url):
    full_url = 'https://' + url
    r = requests.get(full_url)
    return r


def test_url(url_data):
    r = timed_get(url_data['url'])
    url_data['ok'] = r[0].ok
    url_data['response_times'].append(r[1])
    url_data['response_times'].pop(0)
    url_data['avg'] = sum(url_data['response_times']) / len(url_data['response_times'])
    jb.update(url_data, JSONBOX_ID, url_data['_id'], api_key=API_KEY)


def update_urls():
    urls = jb.read(JSONBOX_ID)
    for url in urls:
        test_url(url)


if __name__ == '__main__':
    update_urls()
