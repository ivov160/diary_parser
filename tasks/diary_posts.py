import os
from urllib.parse import urlparse
from urllib import parse

import diary
import tasks

class task():
    def __init__(self, user_id, fails=0, offset=0):
        self.user_id = user_id
        self.offset = offset
        self.fails = fails

    def __str__(self):
        return 'diary_posts.task [ user_id: {}, offset: {}, fails: {} ]'.format(self.user_id, self.offset, self.fails)


def handler(task, ctx):
    #print('diary_posts.handler, task: {}, ctx: ...'.format(task))

    result = []
    #too long fail sequence perhaps end
    if task.fails < ctx.fail_count:
        data = diary.api.api.posts(ctx.sid, task.user_id, task.offset)
        code = diary.api.api.get_code(data)

        #code=0 is ok, other somthing wrong
        if code == 0:
            if task.offset == 0:
                result.append(tasks.diary_posts.task(task.user_id + 1))

            #try load next part if already 0 then stop go in deep
            if len(data['posts']):
                result.append(tasks.diary_posts.task(task.user_id, 0, task.offset + 20))

            #processing posts
            for post in data['posts']:
                result.append(tasks.post_filter.task(data['posts'][post]))
        else: 
            #inc fails counter
            if task.offset == 0:
                result.append(tasks.diary_posts.task(task.user_id + 1, task.fails + 1))

    return result
            



