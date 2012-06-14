from smush import Smush
from config import STRIP_JPG_META

smusher = Smush(strip_jpg_meta=STRIP_JPG_META, exclude=['.bzr', '.git', '.hg', '.svn'], list_only=False, quiet=False, identify_mime=True)
