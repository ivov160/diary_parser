import os, json

import multiprocessing 
import logging
import logging.handlers

class task():
    def __init__(self, data):
        self.data = data

    def __str__(self):
        return 'file_writer.task [ data: ... ]'

def handler(task, ctx):
    print('file_writer.handler, task: ..., ctx: ...')
    logger = logging.getLogger(ctx.tag)
    logger.log(logging.INFO, json.dumps(task.data))

            



