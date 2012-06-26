from config import *
import core
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time
import logging
from path import path

running = False

class CompressionHandler(FileSystemEventHandler):
    def handle_event(self, event):
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

def start(dirs):
    global running
    running = True
    event_handler, observer = CompressionHandler(), Observer()
    for dir in dirs:
        dir = path(dir).abspath()
        if dir.isdir():
            observer.schedule(event_handler, path=dir, recursive=True)
            logging.warning('watching %s', dir)
        else:
            logging.warning('%s is not a directory', dir)
    if not observer._watches:
        logging.error('No valid directories specified. Exiting')
        return
    
    observer.start()
    logging.info('waiting for files')
    logging.info('Ctrl-C to quit')
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


