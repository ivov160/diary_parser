from multiprocessing import Pool
import os

class sheduler:
    def __init__(self, pool_size):
        self.pool_size = pool_size
        self.pool = None
    
    def run(self):
        if self.pool == None:
            self.pool = Pool(self.pool_size)

    def add_task(self, task, task_done, task_failed):
        return self.pool.apply_async(func=task, callback=task_done, error_callback=task_failed)

    def stop(self):
        self.pool.close()
        self.pool.join()

