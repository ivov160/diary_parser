import sys
import os
import argparse

from loader import *
from sheduler import *

def get_posts(sid, begin, end):
    print('get posts, sid: {}, begin: {}, end: {}'.format(sid, begin, end))

def get_session(user, password, apikey):
    print('get session')

def main():
    parser = argparse.ArgumentParser(description='diar.ru post parser')

    date_range = parser.add_argument_group('date range')
    date_range.add_argument('-b', '--begin', help='begin date range')
    date_range.add_argument('-e', '--end', help='end date range')

    account_args = parser.add_argument_group('account settings')
    account_args.add_argument('-u', '--user', help='account username')
    account_args.add_argument('-p', '--password', help='account password')
    account_args.add_argument('-k', '--apikey', help='application key')

    session_args = parser.add_argument_group('session settings')
    parser.add_argument('-s', '--session', help='session id')

    args = parser.parse_args()

    s = sheduler.sheduler()
    s.add_child(get_session);

    #if args.session is not None:
        #get_posts(sid=args.session, begin=args.begin, end=args.end)
    #else:
        #get_posts(sid=get_session(user=args.user, password=args.password, apikey=args.apikey), begin=args.begin, end=args.end)


sys.path.append('./')
if __name__ == '__main__':
    main()

