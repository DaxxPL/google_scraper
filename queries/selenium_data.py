from selenium import webdriver
import re
from bs4 import BeautifulSoup


def give_results(query):
    driver = webdriver.Firefox()
    driver.get(f'https://www.google.com/search?q={query}&num=15')
    soup = BeautifulSoup(driver.page_source, "html5lib")
    num = soup.select('#resultStats')[0].getText()
    num = num.replace('\xa0', '')
    num = int(re.findall(r'\s\d+', num)[0])
    out = [num, ]
    results = soup.find_all('div', class_='g')
    rank = 1
    for item in results:
        link = item.a.get('href')
        try:
            title = item.h3.getText()
        except AttributeError:
            continue
        text_field = item.find(class_='st')
        try:
            text_field.span.replace_with(' ')
        except AttributeError:
            pass
        try:
            text = text_field.getText()
        except AttributeError:
            continue
        out.append({'title': title,
                    'link': link,
                    'text': text,
                    'rank': rank,
                    })
        rank += 1
    driver.close()
    return out
