import os

import diary
import tasks

class task():
    def __init__(self, user_id):
        self.user_id = user_id

    def __str__(self):
        return 'bruteforce_user_id.task [ user_id: {} ]'.format(self.user_id)


def handler(task, ctx):
    #print('bruteforce_user_id.handler, task: {}, ctx: ...'.format(task))

    result = []

    if task.user_id < ctx.max_value:
        stage_max = task.user_id + ctx.step
        for i in range(task.user_id, stage_max):
            result.append(tasks.diary_posts.task(i))

        result.append(tasks.bruteforce_user_id.task(stage_max))

    return result
            



