from urllib.request import urlopen
from bs4 import BeautifulSoup


def get_soup(url):
    try:
        page = urlopen(url).read()
    except Exception as e:
        print('Got an exception: ', e)
        return BeautifulSoup()
    else:
        return BeautifulSoup(page, 'html.parser')


def get_all_text_tags(soup):
    tags = ['p'] + ['h' + str(i) for i in range(1, 7)]
    return soup(tags, string=True)


def get_all_img_tags(soup):
    return soup('img')
