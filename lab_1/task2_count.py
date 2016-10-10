from bs4 import BeautifulSoup

data = ''

with open('result_1.xml') as f:
    data = f.read()

soup = BeautifulSoup(data, features='xml')
pages = soup.find_all('page')

page_with_max_texts = max(pages, key=lambda page: len(page.find_all('fragment', attrs={'type': 'text'})))

print(len(page_with_max_texts.find_all('fragment', attrs={'type': 'text'})))
