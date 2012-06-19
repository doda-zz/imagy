# -*- coding: utf-8 -*-

# all uppercase
from config import *

from utils import make_path, same_file, MARK
from store import store
from smushing import compress_image
import watch
from path import path
import logging

def revert():
    '''Move stored originals back to their initial location'''
    # sort so we move as much as possible before asking what to do
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
                # we still want to go down and remove the file from store so we don't ask for it again
                move = False
        if move:
            logging.info('moving %s back to %s', storedat, pth)
            path(storedat).move(pth)
        del store.originals[pth]
        del store.storedat[storedat]

def clear():
    '''Clear out internal records - this makes --revert unreliable'''
    cleared = len(store.originals)
    store.clear()
    store.save()
    logging.info('cleared %s file names from internal store', cleared)

def handle_evented_file(pth):
    '''handles a file after an event has been received for it'''
    if not store.wants(pth):
        return
    print pth ,store.storedat
    print pth in store.storedat
    if pth in store.storedat:
        if not store.storedat[pth]:
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
            store_original(pth, store.originals[pth])
        else:
            store_original(pth)
    # the original gets briefly added to ignore so watchdog doesnt pick it up
    ignore_file(pth)
    compress_image(pth)
    if KEEP_ORIGINALS and same_file(storedat, pth):
        storedat.remove()
            
def initialize(*dirs):
    '''Run through the specified directories, optimizing all images'''
    logging.info('looking for not yet optimized files')
    dofiles(p for dir in dirs for p in dir.walkfiles())

def do_files(*pths):
    '''Optimize all given files'''
    touched_files = set(pth for kv in store.originals.items() for pth in kv)
    for pth in [path(p).abspath() for p in files]:
        if not pth in touched_files:
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
    '''Store the original'''
    # get an unused file name to store the original
    if not storedat:
        storedat = find_storage_space(pth)
    ignore_file(storedat)
    logging.debug('pushing original to %s', storedat)
    pth.copy(storedat)
    # check if the copy was successful
    if not same_file(pth, storedat):
        raise AttributeError('copy seems to differ from original')
    # and store the original path so we can revert it later
    store.originals[pth] = storedat
    store.storedat[storedat] = None
    return storedat

def find_storage_space(pth, identifier=ORIGINAL_IDENTIFIER):
    '''Find a new path with the identifier'''
    name, ext = pth.splitext()
    return make_path(name + identifier + ext, sep='').abspath()

def ignore_file(pth, store=store):
    '''before touching a file we tell store how many events it should ignore for it'''
    if not watch.running:
        return
    print 'ignoring', pth
    # if the file doesnt exist watchdog sends create and modify else just modify
    n = 1 if pth.exists() else 2
    store.ignore(pth, n)

def correct_ext(pth, exts=IMAGE_EXTENSIONS):
    return pth.splitext()[1] in exts
