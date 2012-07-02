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

parser = optparse.OptionParser('Optimize images')

true_flag = partial(parser.add_option, action="store_true", default=False)
true_flag('-c', '--clear', help=clear.__doc__)
true_flag('-l', '--list', help=list_files.__doc__)
true_flag('-r', '--revert', help=revert.__doc__)
true_flag('-f', '--files', help=do_files.__doc__)
true_flag('-q', '--quiet', help='no output')
true_flag('-m', '--memorystore', help='store internals in memory')
true_flag('--deloriginals', help=delete_originals.__doc__)
true_flag('--debug', help='set logging to DEBUG')
true_flag('--no-init', dest='no_init', help='do not check directories for not yet optimized files')

parser.add_option('-n', '--run', help='Run the daemon '
                  'even though another option has been specified')
parser.add_option('-d', '--dir', action="store", default=STORE_PATH, dest="store_path", help='the directory '
                  'within which internal storage resides')
#debug
true_flag('--dump', help=dump.__doc__)
opts, args = parser.parse_args(sys.argv[1:])

def _main(opts, args):
    level = logging.DEBUG if opts.debug else logging.INFO
    logging.basicConfig(format=FORMAT, level=level)
    
    if opts.quiet:
        logging.disable(logging.CRITICAL)
        
    logging.info('Imagy started')
    logging.debug(map(str, (args, opts)))
    
    if not opts.memorystore:
        store_path = opts.store_path
        if store_path is None:
            imagy_at_home = path('~/%s' % IMAGY_DIR_NAME).expanduser()
            logging.info('Storing settings in %s, you can modify this path in config.py under STORE_PATH',
                         imagy_at_home)
            store_path = imagy_at_home
        store.load(store_path)
        
    args = [path(arg) for arg in args or FILE_PATTERNS if arg]
    run_daemon = opts.run

    if opts.clear: clear()
    elif opts.dump: dump(store)
    elif opts.revert: revert()
    elif opts.list: list_files()
    elif opts.files: do_files(*args)
    elif opts.deloriginals: delete_originals()
    else: run_daemon = True

    if run_daemon:
        # if nothing specified so far, just run `smart mode` i.e. initialize the directories
        # and then run the daemon afterwards
        if not opts.no_init:
            initialize(*args)
        watch.start(args)
    
def main():
    try:
        _main(opts, args)
    finally:
        try:
            store.save()
        except Exception, e:
            logging.error('unable to save %s', str(e))
        else:
            logging.debug('saved to %s', store.dir)
            
if __name__ == '__main__':
    main()
