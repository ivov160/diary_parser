import signal, os

import argparse
import configparser
import datetime

import diary
import sheduler

from time import sleep
from urllib.parse import urlparse
from urllib import parse

class diary_list_task():
    def __init__(self, offset):
        self.offset = offset

    def __str__(self):
        return 'diary_list_task [ offset: {} ]'.format(self.offset)

class diary_posts_task():
    def __init__(self, url, begin, end):
        self.url = url
        self.begin = begin
        self.end = end

        u = urlparse(url)
        domain = u.hostname
        self.short_name = domain[:domain.find('.diary.ru')]

    def __str__(self):
        return 'diary_posts_task [ url: {}, begin: {}, end: {}, short_name: {} ]'.format(
            self.url, self.begin, self.end, self.short_name)


def diary_list_task_handler(task):
    h = diary.html.new(None)
    data = h.get_diary_list(task.offset)

    tasks = []
    if data['next']:
        url = urlparse(data['next'])
        query = parse.parse_qs(url.query)
        if query.get('from'):
            tasks.append(diary_list_task(query['from'][0]))

    #for link in data['links']:
        #tasks.append(diary_posts_task(link, 0, 0))

    return tasks

def diary_posts_task_handler(task):
    api = diary.api.new(None)
    data = h.get_diary_list(task.offset)

def main():
    parser = argparse.ArgumentParser(description='diar.ru post parser')
    parser.add_argument('-c', '--config', required=True, help='path to config file')
    #parser.add_argument('-b', '--begin', required=True, help='begin date range')
    #parser.add_argument('-e', '--end', required=True, help='end date range')

    args = parser.parse_args()
    if args.config is None:
        parser.print_help()
        sys.exit(-1)

    config = configparser.ConfigParser()
    if config.read(args.config, encoding='utf-8') is None:
        print ('can\'t load config file, path: {}'.format(args.config))
        sys.exit(-1)

    #api = diary.api.new(config)
    #if not api.auth():
        #sys.exit(-1)
    #api.posts()

    dispatcher = {
        diary_list_task: diary_list_task_handler,
    }

    s = sheduler.mnager.new(4, sheduler.task_queue.new(1), dispatcher)
    s.add_task(diary_list_task(0))
    s.run()

if __name__ == '__main__':
    main()

