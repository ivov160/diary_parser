import os
import requests
import hashlib
import datetime

class credentials():
    def __init__(self, username, password, public_key, secret_key):
        self.username = username
        self.password = password
        self.public_key = public_key
        self.secret_key = secret_key

class session():
    def __init__(self, sid, expired=datetime.datetime.now()):
        self.sid = sid
        self.expired = expired

        self.touch()

    def is_expired(self):
        return self.expired <= datetime.datetime.now()

    def touch(self):
        self.expired = datetime.datetime.now() + datetime.timedelta(minutes=20)

    def __str__(self):
        return 'api.session [ sid: {}, expired: {} ]'.format(self.sid, self.expired.timestamp())

class api:
    endpoint = 'http://www.diary.ru/api/'

    @staticmethod
    def auth(c):
        md5 = hashlib.md5()
        md5.update(c.secret_key.encode())
        md5.update(c.password.encode())

        params = {
            'method': 'user.auth',
            'username': c.username,
            'password': md5.hexdigest(),
            'appkey': c.public_key
        }

        r = requests.get(api.endpoint, params).json()
        code = api.get_code(r)

        if code != 0:
            raise RuntimeError('failed get sid, code: {}, msg: {}'.format(code, r['error']))

        return session(r['sid'])

    @staticmethod
    def posts(sid, user_id, offset=0):
        if sid.is_expired():
            raise RuntimeError('sid is expired, sid: {}'.format(sid.expired))

        params = {
            'method': 'post.get',
            'sid': sid.sid,
            'type': 'diary',
            'juserid': user_id,
            'from': offset,
            #'fields': 'postid,title,juserid,jaccess,dateline_date,message_html'
        }
        r = requests.get(api.endpoint, params)

        sid.touch()
        return r.json()

    @staticmethod
    def get_code(r):
        code = None
        if r and r['result']:
            code = int(r['result']) 
        return code

