Imagy - make your website's images load upto 50% faster
===============

Imagy uses *lossless compression* on images, so your users never have to load unnecessary bytes. The algorithms used are lossless, so your images look the same, but load faster.

Instead of having to code up deamons, file watches and handle different file formats on your own, Imagy does all the work for you. Just point it at the folder(s) your images are stored in and it will automatically look for files that are created or changed and optimize them for size *without any visual impact*.

Getting Started
-----------------

::

    pip install imagy
    
    imagy /awesome/images/in/here/
    

That's it. Imagy's now running.


You can instead also specifiy the image paths directly in ``config.py`` which already holds a couple of examples


Example
-----------------

As soon as the file

::

    images/img.jpg

gets created, Imagy optimizes it while keeping the original at 

::

    images/img-original.jpg
     

The algorithms used are stable (don't further modify files after multiple invocations), however by default Imagy keeps the original file. If you would not like to keep original images around set KEEP_ORIGINALS to False. 

In the background Imagy uses the awesome library smush which exposes a general interface to handle the various file types.


Further Usage
-----------------


If you wish to stop using Imagy, run ``imagy -r`` which will copy all original images back to their initial location

If you have (rightfully) come to the conclusion that you don't really need to keep originals around, set ``KEEP_ORIGINALS`` in ``config.py`` to  ``False``. If you want to delete all already stored originals run ``imagy --deloriginals``.
