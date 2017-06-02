from multiprocessing import Pool
import multiprocessing 
import logging
import logging.handlers

class logger_config(): 
    def __init__(self, queue, tag, file, configurator):
        self.tag = tag
        self.file_name = file

        self.queue = queue
        self.configurator = configurator

    def __call__(self):
        return self.configurator(self)

class logger():
    def __init__(self, tag, file_name):
        self.__tag = tag
        self.__file_name = file_name
        
        self.__queue = multiprocessing.Queue(-1)
        self.__writer = multiprocessing.Process(
            target=logger.log_writer_process,
            args=(self.get_server_config(), )
        )

    def run(self):
        self.__writer.start()

    def stop(self):
        self.__writer.terminate()
        self.__writer.join()

    @staticmethod
    def log_writer_process(logger_config):
        #call config, for configure logger for this process
        logger_config()

        log_queue = logger_config.queue
        log_tag = logger_config.tag

        while True:
            try:
                msg = log_queue.get()
                logger = logging.getLogger(log_tag)
                logger.handle(msg)
            except Exception:
                import sys, traceback
                print('exception:', file=sys.stderr)
                traceback.print_exc(file=sys.stderr)

    def get_client_config(self):
        return logger_config(
                self.__queue,
                self.__tag,
                self.__file_name,
                logger.client_configure)

    def get_server_config(self):
        return logger_config(
                self.__queue,
                self.__tag,
                self.__file_name,
                logger.server_configure)

    @staticmethod
    def client_configure(config):
        h = logging.handlers.QueueHandler(config.queue)
        l = logging.getLogger(config.tag)

        l.addHandler(h)
        l.setLevel(logging.INFO)

    @staticmethod
    def server_configure(config):
        l = logging.getLogger(config.tag)
        f = logging.Formatter('%(message)s,')
        h = logging.handlers.WatchedFileHandler(config.file_name, 'w')
        h.setFormatter(f)
        l.addHandler(h)

def new(tag, file_name):
    return logger(tag, file_name)
