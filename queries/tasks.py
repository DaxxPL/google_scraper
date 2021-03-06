from __future__ import absolute_import, unicode_literals

import re
from collections import Counter

import celery
from bs4 import BeautifulSoup
from celery import states
from celery.exceptions import SoftTimeLimitExceeded
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.support.wait import WebDriverWait
import os
from .models import Query, Link


def count_words(processed_data):
    my_list = [data['text'].strip() + ' ' + data['title'].strip() for data in processed_data[1:]]
    my_list = [re.sub(r'[^\w\s]', '', s) for s in my_list]
    my_list = [re.sub(r'\W*\b\w{1,2}\b', '', s) for s in my_list]
    my_list = [re.sub(r'[0-9]+', '', s) for s in my_list]
    count = Counter(word.lower() for line in my_list
                    for word in line.split())
    return [i[0] for i in count.most_common(10)]


def get_from_google(driver, search_term, test):
    if test == 'aa':
        driver.get(search_term)
    else:
        driver.get(f'https://www.google.pl/search?q={search_term}&num=15')
    WebDriverWait(driver, 3).until(lambda x: x.find_element_by_id("resultStats"))
    source = driver.page_source
    driver.close()
    return source


@celery.task()
def process_data(search_term, client_ip, browser, proxy, test):
    celery.current_task.update_state(state=states.STARTED, meta={'progress': 'downloading data...'})
    try:
        if proxy != '':
            prox = Proxy()
            prox.proxy_type = ProxyType.MANUAL
            prox.http_proxy = proxy
            prox.socks_proxy = proxy
            prox.ssl_proxy = proxy
        if browser == 'Chrome':
            capabilities = DesiredCapabilities.CHROME
            try:
                prox.add_to_capabilities(capabilities)
            except NameError:
                pass
            host = 'selenium-chrome'
        elif browser == 'Firefox':
            capabilities = DesiredCapabilities.FIREFOX
            try:
                prox.add_to_capabilities(capabilities)
            except NameError:
                pass
            host = 'selenium-firefox'
        driver = webdriver.Remote(command_executor=f'http://{host}:4444/wd/hub',
                                  desired_capabilities=capabilities)
        page_source = get_from_google(driver, search_term, test)
        soup = BeautifulSoup(page_source, "html5lib")
        num = soup.select('#resultStats')[0].getText()
        num = num.replace('\xa0', '')
        num = int(re.findall(r'\s\d+', num)[0])
        processed_data = [num, ]
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
            processed_data.append({'title': title,
                                   'link': link,
                                   'text': text,
                                   'rank': rank,
                                   })
            rank += 1
        num_results = processed_data[0]
        popular_words = count_words(processed_data)
        q, created = Query.objects.update_or_create(text=search_term, defaults=dict(
                                                    popular_words=popular_words, num_results=num_results,
                                                    client_ip=client_ip, browser=browser))
        if not created:
            Link.objects.filter(qu=q).all().delete()
        bulk = [Link(qu=q, title=item['title'], link=item['link'],
                     description=item['text'], position=item['rank']) for item in processed_data[1:]]
        Link.objects.bulk_create(bulk)
    except SoftTimeLimitExceeded:
        driver.close()
        raise SoftTimeLimitExceeded('Timeout limit!')
    return "Success!"
