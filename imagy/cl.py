#! /usr/bin/python
# -*- coding: utf-8 -*-

from core import *
from utils import dump
from functools import partial

import sys
import optparse

import logging
# we're running as a command line script, re-enable logging
logging.disable(logging.NOTSET)
FORMAT = '%(asctime)-15s %(levelname)-12s %(message)s'
logging.basicConfig(format=FORMAT, level=logging.DEBUG)


parser = optparse.OptionParser('Optimize images')

true_flag = partial(parser.add_option, action="store_true", default=False)
true_flag('-i', '--init', help=initialize.__doc__)
true_flag('-c', '--clear', help=clear.__doc__)
true_flag('-l', '--list', help=list_files.__doc__)
true_flag('-r', '--revert', help=revert.__doc__)
true_flag('-f', '--files', help=do_files.__doc__)
true_flag('-q', '--quiet', help='no output')
true_flag('-e', '--deloriginals', help=delete_originals.__doc__)

parser.add_option('-n', '--run', help='Run the daemon'
                  'even though another option has been specified')
parser.add_option('-d', '--dir', action="store", default=STORE_LOC, dest="store_loc", help='the folder'
                  'within which internal storage resides')
#debug
true_flag('-u', help=dump.__doc__)
opts, args = parser.parse_args(sys.argv[1:])

def _main(opts, args):
    if opts.quiet:
        logging.disable(logging.CRITICAL)
        
    logging.info('Imagy started')
    logging.info('Ctrl-C to quit')
    store.load(opts.store_loc)
    dirs = [path(arg) for arg in args or FILE_PATTERNS if arg]
    run_daemon = opts.run

    if opts.clear: clear()
    elif opts.u: dump(store)
    elif opts.revert: revert()
    elif opts.init: initialize(*dirs)
    elif opts.list: list_files()
    elif opts.files: do_files(*args)
    elif opts.list: list_files()
    elif opts.deloriginals: delete_originals()
    else: run_daemon = True

    if run_daemon:
        watch.start(dirs)
    
def main():
    try:
        _main(opts, args)
    finally:
        try:
            store.save()
        except Exception, e:
            logging.error('unable to save %s', str(e))
