from multiprocessing import Pool
from time import sleep
import os


class manager:
    def __init__(self, pool_size, queue, dispatcher):
        self.__pool_size = pool_size
        self.__pool = None

        self.__in_progress = 0
        self.__queue = queue

        self.__stoped = True
        self.__k = 2

        self.__dispatcher = dispatcher
    
    def run(self):
        if self.__pool == None:
            self.__pool = Pool(self.__pool_size)
            self.__stoped = False

        while self.__stoped != True:
            if self.__need_feed() and not self.__queue.empty():
                task = self.__queue.pop();
                if task != None:
                    #print('need_feed: {}, in_progress: {}'.format(self.__need_feed(), self.__in_progress))
                    self.__in_progress += 1
                    self.__pool.apply_async(
                            manager.task_handler, (task, self.__dispatcher,),
                            callback=manager.pool_callback_wrapper(getattr(self, 'task_done')), 
                            error_callback=manager.pool_callback_wrapper(getattr(self, 'task_error')))
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

    @staticmethod
    def task_handler(task,  dispatcher):
        #print('task_handler, result: {}'.format(task))
        return dispatcher[task.__class__]()

    @staticmethod
    def pool_callback_wrapper(method):
        def payload_function(result):
            return method(result)
            #return m.task_done(result)
        return payload_function

    def task_done(self, result):
        #print('task_done, result: {}'.format(result))
        self.__in_progress -= 1
        self.add_task(result)

    def task_error(self, result):
        #print('task_error called')
        #print('result: {}'.format(result))
        self.__in_progress -= 1
        
def new(pool_size, queue, dispatcher):
    return manager(pool_size, queue, dispatcher)
