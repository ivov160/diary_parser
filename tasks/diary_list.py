import os
from urllib.parse import urlparse
from urllib import parse

import diary
from tasks import diary_posts

class task():
    def __init__(self, offset):
        self.offset = offset

    def __str__(self):
        return 'diary_list.task [ offset: {} ]'.format(self.offset)


def handler(task, ctx):
    print('diary_list.handler, task: {}, ctx: {}'.format(task, ctx))
    h = diary.html.new(None)
    data = h.get_diary_list(task.offset)

    tasks = []
    #if data['next']:
        #url = urlparse(data['next'])
        #query = parse.parse_qs(url.query)
        #if query.get('from'):
            #tasks.append(diary_posts.task(query['from'][0]))

    #for link in data['links']:
        #tasks.append(diary_posts_task(link, 0, 0))

    return tasks

