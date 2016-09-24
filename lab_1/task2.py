from bs4 import BeautifulSoup
from lab_1.xml_util import get_soup

# class of an item: g-i-tile g-i-tile-catalog
shop_root = 'https://repka.ua'
shop_link = 'https://repka.ua/search/?SITE_GROUP_ID=61309&q=ssd'

soup = get_soup('https://repka.ua/search/?SITE_GROUP_ID=61309&q=ssd')

items = soup.find_all(class_='cat-list-item', limit=20)

report = BeautifulSoup(features='lxml')


def get_tag(name):
    return report.new_tag(name)


def get_img_tag(src):
    res = report.new_tag('img')
    res['src'] = src
    return res


def get_row_tag():
    return get_tag('tr')


def get_data_tag(text=''):
    res = get_tag('td')
    res['style'] = 'padding: 16px'
    res.string = str(text)
    return res


def get_text_tag(name, text=''):
    res = get_tag(name)
    res.string = text
    return res


def get_table():
    table_tag = get_tag('table')
    table_tag['border'] = '1px'
    table_tag['width'] = '80%'
    table_tag['align'] = 'center'

    table_header = get_tag('tr')

    img_tag = get_text_tag('th', 'Image:')

    descr_tag = get_text_tag('th', 'Description:')
    price_tag = get_text_tag('th', 'Price:')

    table_header.append(img_tag)
    table_header.append(descr_tag)
    table_header.append(price_tag)
    table_tag.append(table_header)
    return table_tag


def execute_task_2():
    table = get_table()

    for item in items:
        img_src = item.find('a').find('img').get('data-original')
        img_src = shop_root + img_src if img_src.startswith('/') else img_src

        descr = item.find(class_='cat-list-col item-col-4').get_text().strip()

        price = item.find(class_='price-uah').span.string

        row = get_row_tag()
        img_td = get_data_tag()
        img_td.append(get_img_tag(img_src))
        row.append(img_td)
        row.append(get_data_tag(descr))
        row.append(get_data_tag(price))

        table.append(row)

    report.append(table)

    print(report.prettify())
    report_string = str(report.encode('latin-1')).replace(r'\r\n', '\n').replace(r'\'', '')

    with open('report.html', 'w') as file:
        file.write(report_string[2:])
