Imagy - make your website's images load upto 50% faster
===============

Imagy is a file daemon, that watches your website's media root (where your images are stored) and automatically optimizes image files that are created or modified within. Imagy uses *lossless compression*, so your users never have to load unnecessary bytes. Your images look the same, but load faster.

A lot of work has gone into making it `set-and-forget`. Instead of having to code up deamons, file watches and handle different file formats on your own, Imagy does all the work for you. All you need to do is
::

    imagy /awesome/images/
    

The algorithms used are stable (don't further modify files after multiple invocations), however to make trying it out as easy as possible Imagy, by default, keeps the original file around for later reversal. 

If you wish to stop using Imagy, run ``imagy -r`` which will copy all original images back to their initial location

If you have (rightfully) come to the conclusion that you don't really need to keep originals around, set ``KEEP_ORIGINALS`` in ``config.py`` to  ``False``. If you want to delete all already stored originals run ``imagy --deloriginals``.


Getting Started 
-----------------

Tested on Ubuntu 11.10:

::

    sudo apt-get install pngnq pngcrush imagemagick gifsicle libjpeg-progs

    pip install imagy
    

That's it. Try it by running ``imagy``.

.. _Information on how to install ``pip``: http://www.pip-installer.org/en/latest/installing.html#prerequisites


Example Usage
-----------------

When starting out you can tell Imagy to optimize (initialize) a directory of new images:

::

    $ ll img
    total 52K
    -rw-rw-r-- 1 ddd ddd 50K 2012-06-23 14:45 beach.jpg
    $ imagy --init img
    2012-06-23 14:48:27,133 INFO         Imagy started
    2012-06-23 14:48:27,133 INFO         Storing settings in /home/ddd/.imagy, you can modify this path in config.py under STORE_PATH
    2012-06-23 14:48:27,134 INFO         looking for not yet optimized files
    2012-06-23 14:48:27,134 INFO         Compressing file /home/ddd/img/beach.jpg
    $ ll img
    total 80K
    -rw-rw-r-- 1 ddd ddd 25K 2012-06-23 14:48 beach.jpg
    -rw-rw-r-- 1 ddd ddd 50K 2012-06-23 14:48 beach-original.jpg

Afterwards you can let imagy start watching the directory (and all directories underneath it) by 

::

    $ imagy img
    2012-06-23 14:52:24,794 INFO         Imagy started
    2012-06-23 14:52:24,794 INFO         Storing settings in /home/ddd/.imagy, you can modify this path in config.py under STORE_PATH
    2012-06-23 14:52:24,795 WARNING      watching /home/ddd/img
    2012-06-23 14:52:24,796 INFO         waiting for files
    2012-06-23 14:52:24,796 INFO         Ctrl-C to quit

As soon as the file


Homage
-----------------

In the background Imagy uses the awesome library smush which exposes a general interface to handle the various file types.



Dependencies
-----------------

imagemagick
gifsicle
jpegtran (on ubuntu in libjpeg-progs)
pngcrush
pngnq 
