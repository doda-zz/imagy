# -*- coding: utf-8 -*-

# all uppercase
from config import *

from utils import make_path, same_file, MARK
from store import store
from libsmush import compress_with_touch
import watch
from path import path
import logging
logging.disable(logging.CRITICAL)

def revert():
    '''Move stored originals back to their initial location'''
    # sort to get as many un-marked paths that require no user input, until prompting for further instruction
    logging.info('reverting %s files', len(store.originals))
    for pth, storedat in sorted(store.originals.items(), key=lambda (k, v):store.storedat[v]):
        move = True
        if store.storedat[storedat] == MARK:
            # the stored original has been modified, wat do?
            resp = raw_input('%s has been modified, move back to %s? [y]es/[N]o/[a]bort ' %
                             (storedat, pth)).lower()[:1]
            if resp == 'a':
                break
            if resp != 'y':
                # we still want to go down and remove the file from store so we don't ask for it
                # upon repeated invocation
                move = False
        if move:
            logging.info('moving %s back to %s', storedat, pth)
            path(storedat).move(pth)
        clear_record(pth, storedat)

def clear_record(pth, storedat):
    '''remove the file from internal storage'''
    del store.originals[pth]
    del store.storedat[storedat]

def clear():
    '''Clear out all internal records - this makes --revert unreliable'''
    cleared = len(store.originals)
    store.clear()
    store.save()
    logging.info('cleared %s file names from internal store', cleared)

def handle_evented_file(pth):
    '''handles a file after an event has been received for it'''
    if not store.wants(pth):
        return
    if pth in store.storedat:
        if not store.storedat[pth]:
            # only warn on first modification
            logging.warning('%s, a stored original has been modified - will ask what to do at --revert', pth)
            store.storedat[pth] = MARK
    else:
        return handle_file(pth)

def handle_file(pth):
    '''Optimizes an image and stores an original if KEEP_ORIGINALS is set'''
    logging.info('Compressing file %s', pth)
    if KEEP_ORIGINALS:
        if pth in store.originals:
            # we have previously optimized this file and know where to store it
            storedat = store_original(pth, store.originals[pth])
        else:
            storedat = store_original(pth)
    # the original gets briefly added to ignore so watchdog doesnt pick it up
    ignore_file(pth)
    compress_with_touch(pth)
    if KEEP_ORIGINALS:
        # only keep the file if we actually optimized it
        if same_file(storedat, pth):
            storedat.remove()
        else:
            store_original_location(pth, storedat)
            
def initialize(*dirs):
    '''Run through the specified directories, optimizing all images'''
    logging.info('looking for not yet optimized files')
    files = (p for dir in dirs for p in dir.walkfiles())
    do_files(*files)

def do_files(*files):
    '''Optimize all given files'''
    touched_files = set(pth for kv in store.originals.items() for pth in kv)
    for pth in [path(p).abspath() for p in files]:
        if pth in touched_files:
            logging.info('ignoring %s', pth)
        else:
            handle_file(pth)
            
def list_files():
    '''list all files in internal store'''
    logging.info('optimized files:')
    i = 0
    for i, (pth, storedat) in enumerate(store.originals.iteritems()):
        print pth, '->', storedat
        i += 1
    logging.info('%s files', i)
        
def store_original(pth, storedat=None):
    '''Store a copy of the original and return its location'''
    if not storedat:
        # get an unused file name to store the original
        storedat = find_storage_space(pth)
    ignore_file(storedat)
    logging.debug('pushing original to %s', storedat)
    pth.copy(storedat)
    # check if the copy was successful
    if not same_file(pth, storedat):
        raise AttributeError('copy seems to differ from original')
    return storedat

def store_original_location(pth, storedat):
    '''store the original path so we can revert it later'''
    store.originals[pth] = storedat
    store.storedat[storedat] = None

def find_storage_space(pth, identifier=ORIGINAL_IDENTIFIER):
    '''Find a new path with the identifier'''
    name, ext = pth.splitext()
    return make_path(name + identifier + ext, sep='').abspath()

def ignore_file(pth, store=store):
    '''before touching a file we tell store how many events it should ignore for it'''
    if not watch.watcher.running:
        return
    # if the file doesnt exist watchdog sends create and modify else just modify
    n = 1 if pth.exists() else 2
    store.ignore(pth, n)

def correct_ext(pth, exts=IMAGE_EXTENSIONS):
    return pth.splitext()[1] in exts

def delete_originals():
    '''Delete all originals, useful if you want to switch KEEP_ORIGINALS to False'''
    for pth, storedat in store.originals.items():
        logging.debug('removing %s', storedat)
        # using remove_p as it doesnt raise an exc if the path doesnt exist
        storedat.remove_p()
        clear_record(pth, storedat)
