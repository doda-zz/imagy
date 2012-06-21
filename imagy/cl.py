#! /usr/bin/python
# -*- coding: utf-8 -*-

from core import *
from utils import dump

import sys
import optparse

import logging
# we're running as a command line script, re-enable logging
logging.disable(logging.NOTSET)
FORMAT = '%(asctime)-15s %(levelname)-12s %(message)s'
logging.basicConfig(format=FORMAT, level=logging.DEBUG)

parser = optparse.OptionParser('Optimize images')
parser.add_option('-i', '--init', action="store_true", default=False, help=initialize.__doc__)
parser.add_option('-c', '--clear', action="store_true", default=False, help=clear.__doc__)
parser.add_option('-l', '--list', action="store_true", default=False, help=list_files.__doc__)
parser.add_option('-r', '--revert', action="store_true", default=False, help=revert.__doc__)
parser.add_option('-f', '--files', action="store_true", default=False, help=do_files.__doc__)
parser.add_option('-q', '--quiet', action="store_true", default=False, help='no output')

parser.add_option('-n', '--run', action="store_true", default=False, help='Run the daemon'
                  'even though another option has been specified')
parser.add_option('-d', '--dir', action="store", default=STORE_LOC, dest="store_loc", help='the folder'
                  'within which internal storage resides')
#debug
parser.add_option('-u', action="store_true", default=False, help=dump.__doc__)
opts, args = parser.parse_args(sys.argv[1:])

def _main(opts, args):
    if opts.quiet:
        logging.disable(logging.CRITICAL)
        
    logging.info('Imagy started')
    logging.info('Ctrl-C to quit')
    store.load(opts.store_loc)
    dirs = map(path, args or FILE_PATTERNS)
    nothing_has_run = None    # False is technincally false here~


    if opts.clear: clear()
    elif opts.u: dump(store)
    elif opts.revert: revert()
    elif opts.init: initialize(*dirs)
    elif opts.list: list_files()
    elif opts.files: do_files(*args)
    elif opts.list: list_files()
    else: nothing_has_run = True

    if opts.run or nothing_has_run:
        watch.start(dirs)
    
def main():
    try:
        _main(opts, args)
    finally:
        try:
            store.save()
        except Exception, e:
            logging.error('unable to save %s', str(e))
