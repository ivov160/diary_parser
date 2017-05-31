import os
import requests

#from bs4 import BeautifulSoup
from lxml import etree
from requests.exceptions import HTTPError

class html:
    def __init__(self, config):
        #mb need added reading headers from config
        #as example config['diary']['headers']
        self.__def_headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36',
        }
        #as example config['diary']['attempts']
        self.__attempts = 5
        self.__delay = 3

    def load_url(self, page_url, stream=False):
        for i in range(self.__attempts):
            try:
                response = requests.get(page_url, headers=self.__def_headers, stream=stream)
                response.raise_for_status()
            except HTTPError as e:
                print (RED.format('page responded with {}. trying again: {}'.format(response.status_code, page_url)))
                time.sleep(self.__delay)
            else:
                return response
        else:
            # failed to get the page raise an exception
            response.raise_for_status()

    def get_parser(self, data):
        parser = etree.HTMLParser()
        return etree.fromstring(data, parser=parser)
        # return BeautifulSoup(data, "lxml")

    def get_diary_list(self, offset):
        url_template = 'http://www.diary.ru/list/?from={}'

        response = self.load_url(url_template.format(offset))
        parser = self.get_parser(response.text)

        links = parser.xpath("//td[contains(@class, 'l')]/a[contains(@class, 'withfloat')]/@href")
        link = parser.xpath("concat('http://www.diary.ru', string(//div[contains(@class, 'pages')]//tr[contains(@class, 'pages_str')]//td[2]/a/@href))")

        return {
            'links': links,
            'next': link
        }

def new(config):
    return html(config) 

