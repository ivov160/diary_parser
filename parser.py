import os, signal

import argparse
import configparser
import datetime

import multiprocessing 
import logging
import logging.handlers

import diary
import sheduler
import tasks


class dispatcher():
    class api_context():
        def __init__(self, config):
            c = diary.api.credentials(
                config['account']['username'],
                config['account']['password'],
                config['api']['public_key'],
                config['api']['secret_key']
            )
            self.sid = diary.api.api.auth(c)
            self.fail_count = int(config['api']['fail_count'])

        def __str__(self):
            return 'dispatcher.api_context [ sid: {}, max_fails: {} ]'.format(self.sid, self.fail_count)

    class file_context():
        def __init__(self, tag):
            self.tag = tag

        def __str__(self):
            return 'dispatcher.file_context [ tag: {} ]'.format(self.tag)

    class filter_context():
        def __init__(self, begin, end, access=0):
            self.begin = begin
            self.end = end
            self.access = access

        def __str__(self):
            return 'dispatcher.filter_context [ begin: {}, end: {}, access: {} ]'.format(self.begin, self.end, self.access)

    def __init__(self, config, begin, end, logger_tag):
        self.__config = config

        self.__handlers = {
            tasks.diary_posts.task: tasks.diary_posts.handler,
            tasks.post_filter.task: tasks.post_filter.handler,
            tasks.data_extractor.task: tasks.data_extractor.handler,
            tasks.file_writer.task: tasks.file_writer.handler
        }

        self.__contexts = {
            tasks.diary_posts.task: dispatcher.api_context(config),
            tasks.post_filter.task: dispatcher.filter_context(begin, end),
            tasks.data_extractor.task: None,
            tasks.file_writer.task: dispatcher.file_context(logger_tag)
        }

    def __call__(self, task):
        # call handlers with specified context
        return self.__handlers[task.__class__](task, self.__contexts[task.__class__])

def get_start_task():
    return tasks.diary_posts.task(1)

def handler_wrapper(s, l):
    def handler(signum, frame):
        print('Signal handler called with signal', signum)
        s.stop()
        l.stop()
    return handler

def main():
    parser = argparse.ArgumentParser(description='diar.ru post parser')
    parser.add_argument('-c', '--config', required=True, help='path to config file')
    parser.add_argument('-b', '--begin', type=int, required=True, help='begin date range')
    parser.add_argument('-e', '--end', type=int, required=True, help='end date range')

    args = parser.parse_args()
    if args.config is None:
        parser.print_help()
        sys.exit(-1)

    config = configparser.ConfigParser()
    if config.read(args.config, encoding='utf-8') is None:
        raise RuntimeError('can\'t load config file, path: {}'.format(args.config))

    try:
        #original_sigint_handler = signal.signal(signal.SIGINT, signal.SIG_IGN)

        #create logger writer process
        logger = sheduler.logger.new(
                config['output']['tag'],
                config['output']['file'])

        #make logger writer callable config
        logger_config = logger.get_client_config()

        #apply logger config for main process
        #logger_config()

        #create task eval context
        router = dispatcher(config, args.begin, args.end, logger_config.tag)

        #creating task sheduller
        s = sheduler.mnager.new(sheduler.task_queue.new(1), router, 1)

        #add start task to sheduller
        s.add_task(get_start_task())

        #run logger writer process and sheduller
        logger.run();
        s.run(logger_config)

        #signal.signal(signal.SIGINT, original_sigint_handler)
        #signal.signal(signal.SIGINT, handler_wrapper(s, l))
        #signal.signal(signal.SIGTERM, handler_wrapper(s, l))
    except KeyboardInterrupt:
        print("Caught KeyboardInterrupt, terminating workers")
    else:
        print("Normal termination")

    #stop event loop for all child processes
    s.stop()
    logger.stop()

if __name__ == '__main__':
    main()

