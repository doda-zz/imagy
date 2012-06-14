#! /usr/bin/python
# -*- coding: utf-8 -*-

from path import path
import sys
import optparse
from utils import make_path, same_file
from datetime import datetime
from persistence import store
from smushing import smusher
import watch

# all uppercase
from config import *

import logging
logging.basicConfig(level=logging.DEBUG)

def revert():
    '''Move stored originals back to their initial location'''
    for pth, storedat in store.originals():
        logging.info('Moving %s back to %s', storedat, pth)
        storedat.move(pth)

def is_saught_after(pth):
    '''Determine if the file should be optimized'''
    pth = path(pth)
    return not pth.isdir() and not pth in store

def handle_file(pth):
    if is_saught_after(pth):
        logging.info('Compressing file %s', pth)
        compress_image(pth)

def initialize(*pths):
    '''Run through the specified directories, optimizing any and all images'''
    for pth in pths:
        for file in pth.walkfiles():
            handle_file(file)

def list_files():
    for pth in store:
        print pth
    logging.info('%s files', len(store))
        
def store_original(pth, modify=False, identifer=ORIGINAL_IDENTIFIER):
    '''Store the original with the ORIGINAL_IDENTIFIER'''
    # get an unused file name to store the original
    name, ext = pth.splitext()
    storedat = make_path(name + ORIGINAL_IDENTIFIER + ext, '')
    pth.copy(storedat)
    # check if the copy was successful
    if pth != storedat and same_file(pth, storedat):
        # and store the original path so we can revert it later
        store[pth] = storedat
        # we touched this path
        store[storedat] = '!'
        return storedat

def compress_image(pth, modify=False, keep_original=None):
    '''
    Check if we should keep the original and then optimize the image
    '''
    if keep_original is None:
        keep_original = KEEP_ORIGINALS
    pth = path(pth)
    storedat = None
    if keep_original:
        storedat = store_original(pth, modify)
        if not storedat:
            logging.error('couldn\'t store original, aborting')
            return
    # if keep_originals is false, we still have to indicate that this path will be touched
    # so watchdog doesnt pick it up
    if not pth in store:
        store[pth] = '!'
    smusher.smush(pth)
    del store[pth]
    return storedat

def main(opts, args):
    logging.info('Imagy started')
    store.load(opts.store or STORE_LOC)
    dirs = map(path, args or FILE_PATTERNS)
    if opts.clear:
        cleared = store.clear()
        logging.info('cleared %s file names from internal store' % cleared)
    elif opts.revert:
        logging.info('reverting %s files', len(store))
        revert()
    elif opts.init:
        logging.info('looking for not yet optimized files')
        initialize(*dirs)
    elif opts.list:
        list_files()
    else:
        watch.start(dirs)

if __name__ == "__main__":
    parser = optparse.OptionParser('Optimize images')
    parser.add_option('-i', '--init', action="store_true", default=False,
                      help='run optimizations over all directories')
    parser.add_option('-c', '--clear', action="store_true", default=False,
                      help='clear internal record of already optimized file names, (--revert relies on this)')
    parser.add_option('-l', '--list', action="store_true", default=False,
                      help='list all files in internal store')
    parser.add_option('-r', '--revert', action="store_true", default=False, help=revert.__doc__)
    parser.add_option('-f', action="store", dest="file_mode")
    parser.add_option('-p', action="store", default='', dest="store")
    opts, args = parser.parse_args(sys.argv[1:])
    try:
        main(opts, args)
    finally:
        store.sync()
        store.close()
