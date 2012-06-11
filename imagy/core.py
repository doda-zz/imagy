#! /usr/bin/python
# -*- coding: utf-8 -*-

from path import path
from subprocess import call
import sys
import logging
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from smush import Smush
from smush.utils import file_name_hash, PNGNQ_EXT
import optparse
from utils import make_path, same_file
from imagy.persistence import load, processed

# these should all be UPPERCASE
from config import *

if __name__ == '__main__':
    from imagy.persistence import processed
else:
    processed = {}

smusher = Smush(strip_jpg_meta=True, exclude=['.bzr', '.git', '.hg', '.svn'], list_only=False, quiet=False, identify_mime=True)

logging.basicConfig(level=logging.DEBUG)

def revert(dirs, identifer=ORIGINAL_IDENTIFIER):
    '''copy back original files to their original location'''
    pths = ((pth, path(value['origpth'])) for pth, value in processed.iteritems() if value['status'] == 'orig')
    for pth, origpth in pths:
        origpth.move(pth)

def is_saught_after(pth):
    '''Determine if the file should be optimized'''
    pth = path(pth)
    # pngnq has to output to the same folder
    return not pth.isdir() and not pth.endswith(PNGNQ_EXT) and not pth in processed['set']

def initialize(pth):
    '''Run through the specified directories, optimizing any and all images'''
    for file in pth.files():
        compress_image(file)

def store_original(pth, identifer=ORIGINAL_IDENTIFIER):
    '''Store the original with the ORIGINAL_IDENTIFIER'''
    # get an unused file name to store the original
    name, ext = pth.splitext()
    origpth = make_path(name + ORIGINAL_IDENTIFIER + ext, '')
    pth.copy(origpth)
    # check if the copy was successful
    if pth != origpth and same_file(pth, origpth):
        # add it to the internal set so watchdog doesn't interpret it as a new file
        # and store the original path so we can revert just in case
        processed['set'].add(origpth)
        processed[pth] = {'origpth':origpth, 'status':'orig'}
        return origpth

def compress_image(pth, keep_original=None):
    '''
    Check if we should keep the original and then optimize the image, reaching into the lower level ibrary
    '''
    if keep_original is None:
        keep_original = KEEP_ORIGINALS
    pth = path(pth)
    if keep_original:
        origpth = store_original(pth)
        if not origpth:
            logging.error('couldn\'t store original, aborting')
            return
    processed['set'].add(pth)
    smusher.smush(pth)
    return origpth

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

def main(opts, args):
    logging.info('Imagy started')
    if opts.clear:
        cleared = len(processed)
        processed.clear()
        logging.info('cleared %s file names' % cleared)
        exit()
    if opts.init:
        logging.info('looking for not yet optimized files')
        initialize()
    event_handler, observer = CompressionHandler(), Observer()
    dirs = args if args else FILE_PATTERNS
    scheduled = []
    for dir in dirs:
        if not path(dir).isdir():
            logging.warning('%s is not a directory', dir)
        else:
            observer.schedule(event_handler, path=dir, recursive=True)
            scheduled.append(dir)
    if not scheduled:
        logging.error('No valid directories specified. Exiting')
        exit()
    observer.start()
    logging.info('waiting for files')
    try:
        while True:
            time.sleep(0.2)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


if __name__ == "__main__":
    parser = optparse.OptionParser('Optimize images')
    parser.add_option('-i', '--init', action="store_true", default=False, help='run optimizations over all directories')
    parser.add_option('-c', '--clear', action="store_true", default=False, help='clear internal record of already optimized file names')
    parser.add_option('-r', '--revert', action="store_true", default=False, help=revert.__doc__)
    parser.add_option('-d', '--dontrun', action="store_false", default=True, help='do not run the daemon')
    parser.add_option('-f', action="store", dest="file_mode")
    #parser.add_option('-c', action="store", dest="c", type="int")
    opts, args = parser.parse_args(sys.argv[1:])
    try:
        main(opts, args)
    finally:
        save_set()
