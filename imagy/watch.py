from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from config import *
from core import is_saught_after, compress_image
import time
import logging


class CompressionHandler(FileSystemEventHandler):
    def handle_event(self, event):
        pth = path(event.src_path)
        if is_saught_after(pth):
            logging.warning("Compressing %s", pth)
            compress_image(pth)
            logging.warning("Compressed %s", pth)
    
    def on_created(self, event):
        if not OPTIMIZE_ON_CREATE:
            return
        super(CompressionHandler, self).on_created(event)
        time.sleep(SECONDS_AFTER_CREATE)
        self.handle_event(event)
        
    def on_modified(self, event):
        if 1 or not OPTIMIZE_ON_CHANGE:
            return
        super(CompressionHandler, self).on_modified(event)
        time.sleep(SECONDS_AFTER_CHANGE)
        self.handle_event(event)

def start(dirs):
    scheduled = False
    for dir in dirs:
        if not path(dir).isdir():
            logging.warning('%s is not a directory', dir)
        else:
            observer.schedule(event_handler, path=dir, recursive=True)
            scheduled = True
    if not scheduled:
        logging.error('No valid directories specified. Exiting')
        exit()
    
    event_handler, observer = CompressionHandler(), Observer()
    observer.start()
    logging.info('waiting for files')
    try:
        while True:
            time.sleep(0.5)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


