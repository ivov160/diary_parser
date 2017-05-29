from multiprocessing import Pool
import os

def __task_do():
    print('__task_do called')
    #fetch task from queue
    #call task handler in pool context
    
def __task_done(result):
    print('__task_done done called')
    print('result: {}'.format(result))
    #push results to queue

def __task_error(result):
    print('__task_error called')
    print('result: {}'.format(result))
    #error handling

class sheduler:
    def __init__(self, pool_size, queue):
        self.pool_size = pool_size
        self.pool = None
        self.queue = queue
    
    def run(self):
        if self.pool == None:
            self.pool = Pool(self.pool_size)
            self.apply_async(func=__task_do, callback=__task_done, error_callback=__task_error)

    #def add_task(self, task, task_done, task_failed):
        #return self.pool.apply_async(func=task, callback=task_done, error_callback=task_failed)

    def add_task(self, task):
        self.queue.put(task)

    def stop(self):
        self.pool.close()
        self.pool.join()


def new(pool_size, queue):
    return sheduler(pool_size, queue)
