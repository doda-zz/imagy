Imagy - make your website's images load upto 50% faster
===============

As soon as an image in your site's media root gets created or modified, Imagy uses _lossless compression_ on them, so your users never have to load unnecessary bytes. The algorithms used are lossless, so your images look the same, but load faster.

Instead of having to code up deamons, file watches and handle different file formats on your own, Imagy does all the work for you. Just point it at the folder(s) your images are stored in and it will automatically look for files that are created or changed and optimize them for size _without any visual impact_.

Getting Started
-----------------


pip install imagy

imagy /awesome/images/in/here/ /also/here/

That's it. Imagy's now running.


You can instead also specifiy the image paths directly in `config.py` which already holds a couple of examples


Example
-----------------

`images/img.jog`

gets optimized, the original stays at

`images/img-original.jog`

The algorithms used are stable (don't further modify files after multiple invocations), however by default Imagy keeps the original file. If you would not like to keep original images around set KEEP_ORIGINALS to False. 

In the background Imagy uses the awesome library smush which exposes a general interface to handle the various file types. 
