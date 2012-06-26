from path import path

IMAGY_DIR_NAME = '.imagy'

OPTIMIZE_ON_CREATE = True
OPTIMIZE_ON_CHANGE = True

SECONDS_AFTER_CREATE = 0
SECONDS_AFTER_CHANGE = 0

FILE_PATTERNS = (
#    '/srv/images/*',
#    '/home/me/awesome/',
    )

# If set to False, Imagy will delete originals after deletion
KEEP_ORIGINALS = True

#this is inserted before the file extension, if the path already exists, append a 0 to the identifier and keep iterating until a free path is found
ORIGINAL_IDENTIFIER = '-original'

IMAGE_EXTENSIONS = (
    'jpg',
    'jpeg',
    'png',
    'gif',
    )
   
STRIP_JPG_META = True

IMAGE_EXTENSIONS = ['.'+ext for ext in IMAGE_EXTENSIONS]

# the location where imagy stores its internals, if this is `None` at startup, imagy will ask where it should store

STORE_PATH = None
