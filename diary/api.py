import os
import requests
import hashlib

class api:
    def __init__(self, config):
        self.username = config['account']['username']
        self.password = config['account']['password']
        self.secret_key = config['api']['secret_key']
        self.public_key = config['api']['public_key']
        self.endpoint = config['api']['endpoint']
        self.sid = None

    def auth(self):
       md5 = hashlib.md5()
       md5.update(self.secret_key.encode())
       md5.update(self.password.encode())

       params = {
           'method': 'user.auth',
           'username': self.username,
           'password': md5.hexdigest(),
           'appkey': self.public_key
       }

       r = requests.get(self.endpoint, params)
       response = r.json()

       code = int(response['result'])
       if code == 0:
           self.sid = response['sid']
           return True

       print('failed get sid, code: {}, msg: {}'.format(code, response['error']))
       return False

    def posts(self):
       params = {
           'method': 'post.get',
           'sid': self.sid,
           'type': 'diary',
           'shortname': 'sd-nek',
           #'juserid': '3349986',
           'fields': 'postid,title,juserid,jaccess,dateline_cdate,message_html'
       }

       r = requests.get(self.endpoint, params)
       response = r.text
    
       print(response)
       #print('{}'.format(response))

def new(config):
    return api(config) 
