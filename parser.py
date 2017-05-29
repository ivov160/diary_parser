import os
import sys
import argparse
import configparser

from time import sleep

import diary
import sheduler

def task_do():
    print('task do called')

def task_done(result):
    print('task done called')
    print('result: {}'.format(result))

def task_failed(result):
    print('task failed called')
    print('result: {}'.format(result))

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

    api = diary.api.new(config)
    if not api.auth():
        sys.exit(-1)

    api.posts()


    #s = sheduler.sheduler(4)
    #s.run()

    #s.add_task(task_do, task_done, task_failed)

    #s.stop()

    #if args.session is not None:
        #get_posts(sid=args.session, begin=args.begin, end=args.end)
    #else:
        #get_posts(sid=get_session(user=args.user, password=args.password, apikey=args.apikey), begin=args.begin, end=args.end)

if __name__ == '__main__':
    main()

