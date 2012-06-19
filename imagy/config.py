from path import path

OPTIMIZE_ON_CREATE = True
OPTIMIZE_ON_CHANGE = True

SECONDS_AFTER_CREATE = 0
SECONDS_AFTER_CHANGE = 0
FILE_PATTERNS = (
#    '/srv/images/*',
#    '/home/me/awesome/',
    )

# By default wait upto a minute until all other processes have closed the file
MAX_OPEN_FILEHANDLES = 0
MAX_WAIT_OPEN_FILEHANDLES = 60

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

ROOT = path(__file__).parent.abspath()
STORE_LOC = ROOT.joinpath('picklejar')

IMAGE_EXTENSIONS = ['.'+ext for ext in IMAGE_EXTENSIONS]

