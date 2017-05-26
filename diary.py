import sys
import os
import argparse

def get_posts(sid):
    print('get posts\n')

def get_session(user, password, apikey):
    print('get session\n')

def main():
    parser = argparse.ArgumentParser(description='diar.ru post parser')

    account_args = parser.add_argument_group('account settings')
    account_args.add_argument('-u', '--user', help='account username')
    account_args.add_argument('-p', '--password', help='account password')
    account_args.add_argument('-k', '--apikey', help='application key')

    session_args = parser.add_argument_group('session settings')
    parser.add_argument('-s', '--session', help='session id')

    args = parser.parse_args()

    if args.session is not None:
        get_posts(sid=args.session)
    else:
        get_posts(sid=get_session(user=args.user, password=args.password, apikey=args.apikey))


if __name__ == '__main__':
    main()

