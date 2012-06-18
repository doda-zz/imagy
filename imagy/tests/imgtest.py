from path import path
root = path(__file__)
image_loc = root.parent.joinpath('images')
images = {
    'png':'png.png',
    'jpg':'jpg.jpg',
    'gif':'gif.gif',
    'gifgif':'gifgif.gif'
    }
images = dict((k, path(v)) for k, v in images.items())
