self.image_loc = path('images/')
images = {
    'png':'png.png',
    'jpg':'jpg.jpg',
    'gif':'gif.gif',
    'gifgif':'gifgif.gif'
    }
images = dict((k, image_loc.joinpath(v)) for k, v in images.items())
