import signal, os

import argparse
import configparser
import datetime

import diary
import sheduler

from time import sleep

#def get_posts():
    #print('get_posts called')
    ## api = diary.api.new(None)
    ##return api.posts()
    ## return sheduler.task.new('posts_list', None)
    #return "asdasd"


def fast_handler():
    print('fast_handler')
    return Long()

def sleep_handler():
    print('sleep_handler')
    sleep(3)
    return Long()

def long_handler():
    print('long_handler')
    a = 2
    for j in range(0, 100000):
        a += 1
    return Fast()

class Long(): pass
class Sleep(): pass
class Fast(): pass

class diary_list_task():
    def __init__(self, offset, begin, end):
        self.offset = offset
        self.begin = begin
        self.end = end

# def diary_list_task_handler(task):
    

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

    #d = {
        #'fast': fast_handler,
        #'sleep': sleep_handler,
        #'long': long_handler,
    #}

    # d = {
        # Fast: fast_handler,
        # Sleep: sleep_handler,
        # Long: long_handler,
    # }

    # s = sheduler.mnager.new(4, sheduler.task_queue.new(1), d)

    # s.add_task(Fast())
    # #s.add_task('fast')

    # s.run()

    t = diary.html.new(None)
    t.get_diary_list(0, 3, 4)

if __name__ == '__main__':
    main()

