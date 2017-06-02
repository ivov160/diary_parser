import os
from urllib.parse import urlparse
from urllib import parse

import diary
import tasks

class task():
    def __init__(self, user_id, offset, begin, end):
        self.user_id = user_id
        self.offset = offset
        self.begin = begin
        self.end = end

    def __str__(self):
        return 'diary_posts.task [ user_id: {}, offset: {}, begin: {}, end: {} ]'.format(
            self.user_id, self.offset, self.begin, self.end)


def handler(task, ctx):
    print('diary_posts.handler, task: {}, ctx: ...'.format(task))

    result = []
    data = diary.api.api.posts(ctx.sid, task.user_id, task.offset)
    if data:
        #try load next part if already 0 then stop go in deep
        if len(data['posts']):
            result.append(tasks.diary_posts.task(task.user_id, task.offset + 20, task.begin, task.end))

        #processing posts
        for post in data['posts']:
            result.append(tasks.file_writer.task(data['posts'][post]))

    return result
            



