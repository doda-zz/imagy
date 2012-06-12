#! /usr/bin/python
# -*- coding: utf-8 -*-

from path import path
import sys
import optparse
from utils import make_path, same_file, PNGNQ_EXT
from datetime import datetime
from itertools import groupby
import persistence
from persistence import processed
from smushing import smusher

# all uppercase
from config import *

import logging
logging.basicConfig(level=logging.DEBUG)

def revert(processed=processed):
    '''Move stored originals back to their initial location'''
    for origpth, group in groupby(processed['orig'].iteritems(), lambda (k,v): v['origpth']):
        # move the latest original back to the initial location
        storedat = max(group, key=lambda (storedat, info):info['date'])
        logging.info('Moving %s back to %s')
        storedat.move(origpth)

def is_saught_after(pth):
    '''Determine if the file should be optimized'''
    pth = path(pth)
    # pngnq has to output to the same folder
    return not pth.isdir() and not pth.endswith(cfg.PNGNQ_EXT) and not pth in processed['set']

def initialize(pth):
    '''Run through the specified directories, optimizing any and all images'''
    for file in pth.files():
        compress_image(file)

def store_original(pth, identifer=ORIGINAL_IDENTIFIER):
    '''Store the original with the ORIGINAL_IDENTIFIER'''
    # get an unused file name to store the original
    name, ext = pth.splitext()
    storedat = make_path(name + ORIGINAL_IDENTIFIER + ext, '')
    pth.copy(storedat)
    # check if the copy was successful
    if pth != storedat and same_file(pth, storedat):
        # add it to the internal set so watchdog doesn't interpret it as a new file
        # and store the original path so we can revert it later
        processed['set'].add(storedat)
        processed['orig'][storedat] = {'origpth':pth,
                                       'date':datetime.utcnow()}
        return storedat

def compress_image(pth, keep_original=None):
    '''
    Check if we should keep the original and then optimize the image, reaching into the lower level ibrary
    '''
    if keep_original is None:
        keep_original = KEEP_ORIGINALS
    pth = path(pth)
    if keep_original:
        storedat = store_original(pth)
        if not storedat:
            logging.error('couldn\'t store original, aborting')
            return
    processed['set'].add(pth)
    smusher.smush(pth)
    return storedat

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
        exit()

    persistence.init(opts.processed or PROCESSED_LOC)
    watch.start(args or FILE_PATTERNS)

if __name__ == "__main__":
    parser = optparse.OptionParser('Optimize images')
    parser.add_option('-i', '--init', action="store_true", default=False,
                      help='run optimizations over all directories')
    parser.add_option('-c', '--clear', action="store_true", default=False,
                      help='clear internal record of already optimized file names')
    parser.add_option('-r', '--revert', action="store_true", default=False, help=revert.__doc__)
    parser.add_option('-f', action="store", dest="file_mode")
    parser.add_option('-p', action="store", default='', dest="processed_file")
    opts, args = parser.parse_args(sys.argv[1:])
    try:
        main(opts, args)
    finally:
        save_set()


