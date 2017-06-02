import os
import queue

#simple wrapper over mem queue
#needed for replacing implementation (example: redis queue)
class task_queue:
    def __init__(self, timeout):
        self.__queue = queue.LifoQueue()
        self.__timeout = timeout

    def empty(self):
        return self.__queue.empty()

    def push(self, task):
        self.__queue.put(task, timeout=self.__timeout)

    def pop(self):
        return self.__queue.get(timeout=self.__timeout)
    

def new(timeout):
    return task_queue(timeout)
