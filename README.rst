Imagy - make your website's images load upto 50% faster
===============

Imagy is a file daemon, that watches your website's media root (where your images are stored) and automatically optimizes image files that are created or modified within. 

Imagy uses *lossless compression*, so your users never have to load unnecessary bytes. Your images look the same, but load faster.
 
Getting Started 
-----------------

Imagy relies on a few select binaries_ to perform image optimization. On Ubuntu (tested on 11.10) you can install everything with:

.. _binaries: https://github.com/doda/imagy#dependencies

::

    sudo apt-get install pngnq pngcrush imagemagick gifsicle libjpeg-progs

    pip install imagy
    

That's it. 


Running it for the first time
-----------------

A lot of work has gone into making it ``set-and-forget``. If you're running it for the first time, this command should be all you need:
::

    imagy /awesome/images/
    
Imagy will run through the directory ``/awesome/images/`` and all its subdirectories and optimize all image files it finds. After that it will watch these directories for images that get created or modified.

The algorithms used are stable (don't further modify files after multiple invocations), however to make trying Imagy out as easy as possible, the default is to keep original files around for later reversal. For example the file ``/file.jpg`` would be copied to ``/file-original.jpg`` before optimization. If the optimized fileis not smaller than the original, no copy gets stored and the original file remains unchanged.


Further Usage
-----------------

If after some time you wish to stop using Imagy, run ``imagy --revert`` which will move all original images back to their initial location.

If you have (rightfully) come to the conclusion that you don't really need to keep originals around, set ``KEEP_ORIGINALS`` in ``config.py`` to ``False``. If you want to delete all already stored originals run ``imagy --deloriginals``.

Credits
-----------------

In the background Imagy uses the awesome library smush.py_ which exposes a general interface to handle the various file types.

.. _smush.py: https://github.com/thebeansgroup/smush.py

Notes
-----------------

Imagy in production at sc2wow.com_. I was able to save 150kB off my frontpage load, saving anywhere from 5% to 50% per image, though your results may differ.

.. _sc2wow.com: http://sc2wow.com

More information on how to install pip_

.. _pip: http://www.pip-installer.org/en/latest/installing.html#prerequisites


Dependencies
-----------------

- imagemagick
- gifsicle
- jpegtran (on ubuntu in libjpeg-progs)
- pngcrush
- pngnq 
