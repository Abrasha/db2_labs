from lab_1.xml_util import *
import lab_1.write_report as report
import re

task_site = 'http://kpi.ua/'


def get_kpi_soup():
    return get_soup(task_site)


def find_all_http_links(soup, limit=20, recursive=True):
    a_tags = soup.find_all('a', limit=limit, recursive=recursive, attrs={'href': re.compile("^http://")})
    return [a.get('href') for a in a_tags]


def execute_task_1():
    kpi_soup = get_kpi_soup()

    data = {
        task_site: (get_all_text_tags(kpi_soup), get_all_img_tags(kpi_soup))
    }

    for url in find_all_http_links(kpi_soup):
        print('reading url: ', url)
        data[url] = (get_all_text_tags(get_soup(url)), get_all_img_tags(get_soup(url)))

    with open('result_1.xml', 'w') as file:
        file.write(str(report.write_report(data).prettify()))
