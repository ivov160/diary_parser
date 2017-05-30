from multiprocessing import Pool
from time import sleep
import os

def task_done(result):
    print('__task_done done called')
    print('result: {}'.format(result))
    #push results to queue

def task_error(result):
    print('__task_error called')
    print('result: {}'.format(result))
    #error handling

class manager:
    def __init__(self, pool_size, queue):
        self.__pool_size = pool_size
        self.__pool = None

        self.__in_progress = 0
        self.__queue = queue

        self.__stoped = True
        self.__k = 0.5
    
    def run(self):
        if self.__pool == None:
            self.__pool = Pool(self.__pool_size)
            self.__stoped = False

        while self.__stoped != True:
            if self.__need_feed():
                task = self.__queue.pop();
                if task != None:
                    self.__pool.apply_async(func = lambda self, task: __task_do(self, task), callback=task_done, error_callback=task_error)
            else:
                sleep(1)

    def add_task(self, task):
        self.__queue.push(task)

    def stop(self):
        self.__stoped = True
        self.__pool.close()
        self.__pool.join()

    def __need_feed(self):
        return self.__in_progress < self.__pool_size * self.__k

    def __task_do(self, task):
        ++self.__in_progress

        print('__task_do called')
        #fetch task from queue
        #call task handler in pool context
        
def new(pool_size, queue):
    return manager(pool_size, queue)
