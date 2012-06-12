from smush import Smush

smusher = Smush(strip_jpg_meta=True, exclude=['.bzr', '.git', '.hg', '.svn'], list_only=False, quiet=False, identify_mime=True)
