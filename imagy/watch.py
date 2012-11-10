from config import *
import core
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time
import logging
from path import path
import multiprocessing as mp

running = False

class CompressionHandler(FileSystemEventHandler):
    '''Subclassing Watchdog to specify our own handling of files'''
    def handle_event(self, event):
        # convert to an abspath as soon as possible, if relative paths enter the system
        # things start to break
        pth = path(event.src_path).abspath()
        if not pth.isdir() and core.correct_ext(pth):
            core.handle_evented_file(pth)

    def on_created(self, event):
        if not OPTIMIZE_ON_CREATE:
            return
        super(CompressionHandler, self).on_created(event)
        time.sleep(SECONDS_AFTER_CREATE)
        self.handle_event(event)

    def on_modified(self, event):
        if not OPTIMIZE_ON_CHANGE:
            return
        super(CompressionHandler, self).on_modified(event)
        time.sleep(SECONDS_AFTER_CHANGE)
        self.handle_event(event)

class Watcher(object):
    def __init__(self, event_handler_cls, observer_cls=None):
        if observer_cls is None:
            self.observer_cls = Observer
        self.event_handler_cls = event_handler_cls
        self.running = False

    def add(self, *dirs):
        dirs = [path(dir).abspath() for dir in dirs]
        for dir in dirs:
            if dir.isdir():
                self.observer.schedule(self.event_handler, path=dir, recursive=True)
                logging.warning('watching %s', dir)
            else:
                logging.warning('%s is not a directory', dir)

    def run(self, *dirs):
        self.event_handler = self.event_handler_cls()
        self.observer = self.observer_cls()
        self.add(*dirs)
        if not self.observer._watches:
            logging.error('No valid directories specified.')
            return

        self.running = True
        self.observer.start()
        logging.info('waiting for files')
        logging.info('Ctrl-C to quit')
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.observer.stop()
        self.observer.join()

watcher = Watcher(CompressionHandler)
