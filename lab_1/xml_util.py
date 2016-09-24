from urllib.request import urlopen
from bs4 import BeautifulSoup


def get_soup(url):
    try:
        req = urlopen(url)
        encoding = get_charset(req)
        page = req.read().decode(encoding).encode('utf8')

    except Exception as e:
        print('Got an exception: ', e)
        return BeautifulSoup(markup='html.parser')
    else:
        return BeautifulSoup(page, 'html.parser')


def get_charset(req):
    return req.headers['content-type'].split('charset=')[-1]


def get_all_text_tags(soup):
    tags = ['p'] + ['h' + str(i) for i in range(1, 7)]
    return soup(tags, string=True)


def get_all_img_tags(soup):
    return soup('img')
