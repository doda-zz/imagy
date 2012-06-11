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

# If set to False, Image will delete originals after deletion
KEEP_ORIGINALS = True

# To keep things simple, Imagy defaults to holding no internal state as to what images it has already processed and simply looks if a respective original file already exists. Setting WATCH_ORIGINALS to False means 
WATCH_ORIGINALS = True

#this is inserted between the file base name and extension
ORIGINAL_IDENTIFIER = '-original'

IMAGE_EXTENSIONS = (
    'jpg',
    'jpeg',
    'png',
    'gif',
    )
   

PROCESSED_LOC = 'processed.p'
