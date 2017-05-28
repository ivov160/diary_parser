from multiprocessing import Pool
import os

class sheduler:
    def __init__(self, pool_size=os.cpu_count):
        self.pool_size = pool_size
        self.pool = None
    
    def run(self):
        if self.pool == None:
            self.pool = Pool(processes=self.pool_size)

    def add_child(self, func, callback):
        return self.pool.apply_async(func=func,callback=callback)

