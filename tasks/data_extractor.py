import os
import tasks

class task():
    def __init__(self, data):
        self.data = data

    def __str__(self):
        return 'data_extractor.task [ data: ... ]'

def handler(task, ctx):
    print('data_extractor.handler, task: ..., ctx: ...')

    result = []
    post = task.data
    if post:
        item = {
            'date': int(post['dateline_date']),
            'text': post['message_html'],
            'url': 'http://{}.diary.ru/p{}.htm'.format(post['shortname'], post['postid'])
        }
        result.append(tasks.file_writer.task(item))

    return result

            



