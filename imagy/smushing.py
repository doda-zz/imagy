from config import STRIP_JPG_META
from utils import filesig

from smush import Smush
from path import path

smusher = Smush(strip_jpg_meta=STRIP_JPG_META, exclude=['.bzr', '.git', '.hg', '.svn'], list_only=False, quiet=True, identify_mime=True)

def compress_image(pth, smusher=smusher):
    '''
    i feel dirty, but we need to guarantee that watchdog fires an event when the file gets optimized
    '''
    pth = path(pth).abspath()
    sig = filesig(pth)
    smusher.smush(pth)
    if filesig(pth) == sig:
        # no event fired, force it ourselves
        pth.touch()
