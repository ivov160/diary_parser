import multiprocessing 
from multiprocessing import Pool
from time import sleep
import os


class manager:
    def __init__(self, queue, dispatcher, pool_size):
        self.__pool_size = pool_size
        self.__pool = None

        self.__in_progress = 0
        self.__queue = queue

        self.__stoped = True
        self.__k = 16

        self.__dispatcher = dispatcher
    
    def run(self, logger_config):
        if self.__pool == None:
            self.__pool = Pool(processes=self.__pool_size, initializer=manager.init_pool, initargs=[logger_config])
            self.__stoped = False

        while self.__stoped != True:
            #print('shduler.mngr: stopped: {}'.format(self.__stoped))
            if self.__need_feed() and not self.__queue.empty():
                task = self.__queue.pop();
                if task != None:
                    #print('need_feed: {}, in_progress: {}'.format(self.__need_feed(), self.__in_progress))
                    self.__in_progress += 1
                    self.__pool.apply_async(
                            manager.task_handler, (task, self.__dispatcher, ),
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
    def init_pool(logger_config):
        logger_config()

    @staticmethod
    def task_handler(task,  dispatcher):
        try:
            print('task_handler, task: {}'.format(task))
            return dispatcher(task)
        except Exception:
            import sys, traceback
            print('exception:', file=sys.stderr)
            traceback.print_exc(file=sys.stderr)

    @staticmethod
    def pool_callback_wrapper(method):
        def payload_function(result):
            return method(result)
        return payload_function

    def task_done(self, result):
        print('task_done')
        #print('task_done, result: {}'.format(result))
        self.__in_progress -= 1

        if result:
            for task in result:
                #print('add new task: {}'.format(task))
                self.add_task(task)

    def task_error(self, result):
        print('task_error, result: {}'.format(result))
        self.__in_progress -= 1
        
def new(queue, dispatcher, pool_size=16):
    return manager(queue, dispatcher, pool_size)
