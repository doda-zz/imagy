Imagy - make your website's images load upto 50% faster
===============

Imagy is a file daemon, that watches your website's media root (where your images are stored) and automatically optimizes image files that are created or modified within it. Imagy uses *lossless compression*, so your users never have to load unnecessary bytes while the algorithms used are completely lossless. Your images look the same, but load faster.

A lot of work has gone into making it `set-and-forget`. Instead of having to code up deamons, file watches and handle different file formats on your own, Imagy does all the work for you. All you need to do is
::

    imagy /awesome/images/
    

The algorithms used are stable (don't further modify files after multiple invocations), however to make trying it out as easy as possible Imagy, by default, keeps the original file around for later reversal. 

If you wish to stop using Imagy, run ``imagy -r`` which will copy all original images back to their initial location

If you have (rightfully) come to the conclusion that you don't really need to keep originals around, set ``KEEP_ORIGINALS`` in ``config.py`` to  ``False``. If you want to delete all already stored originals run ``imagy --deloriginals``.


Getting Started 
-----------------

Tested on Ubuntu 10.04 & 11.10:

::

    sudo apt-get install pngnq pngcrush imagemagick gifsicle libjpeg-progs

    pip install imagy
    

That's it. You should now be able to run ``imagy``.


.. _Information on how to install ``pip``: http://www.pip-installer.org/en/latest/installing.html#using-the-installer


Example
-----------------

As soon as the file

::

    images/img.jpg

gets created, Imagy optimizes it while keeping the original at 

::

    images/img-original.jpg
     

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
