import os
from urllib.parse import urlparse
from urllib import parse

import diary
import tasks

class task():
    def __init__(self, data):
        self.data = data

    def __str__(self):
        return 'post_filter.task [ data: {} ]'.format(self.data)


def handler(task, ctx):
    #print('post_filter.handler, task: {}, ctx: {} '.format(task, ctx))

    result = []
    post = task.data
    if post:
        if 'jaccess' in post and int(post['jaccess']) == ctx.access:
            if 'dateline_date' in post:
                post_ts = int(post['dateline_date'])
                if post_ts > ctx.begin and post_ts < ctx.end:
                    result.append(tasks.data_extractor.task(post))
    return result
            



