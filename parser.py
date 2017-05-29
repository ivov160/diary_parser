import os
import sys
import argparse
import configparser

from time import sleep

import diary
import sheduler

def get_posts(begin, end):
    api = diary.api.new(None)
    #return api.posts()
    return sheduler.task.new('posts_list', None)


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

    s = sheduler.sheduler.new(4, sheduler.queue.new(1))

    #s.add_task(get_posts(begin, end))
    #s.add_task(task_do, task_done, task_failed)

    s.run()

if __name__ == '__main__':
    main()

