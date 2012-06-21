from path import path
from context import imagy

root = path(__file__)
image_loc = root.parent.joinpath('images')
image_files = {
    'png':'png.png',
    'jpg':'jpg.jpg',
    'gif':'gif.gif',
    'gifgif':'gifgif.gif'
    }
images = dict((k, image_loc.joinpath(v)) for k, v in image_files.items())

def create_img_dir():
    tmp = path(mkdtemp())
    image_loc.copytree(self.tmp)
    return tmp
