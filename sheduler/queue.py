import o
import queue

class queue:
    def __init__(self, timeout):
        self.queue = Queue()
        self.timeout = timeout

    def empty(self):
        return self.queue.empty()

    def push(self, task):
        self.queue.put(task, timeout=self.timeout)

    def pop(self):
        return self.queue.get(timeout=self.timeout)
    

def new(timeout):
    return queue(timeout)
