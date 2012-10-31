import os.path
from ..optimiser import Optimiser

class OptimisePNG(Optimiser):
    """
    Optimises pngs. Uses pngnq (http://pngnq.sourceforge.net/) to quantise them, then uses pngcrush
    (http://pmt.sourceforge.net/pngcrush/) to crush them.
    """


    def __init__(self, **kwargs):
        super(OptimisePNG, self).__init__(**kwargs)

        if kwargs.get('quiet') == True:
            pngcrush = 'pngcrush -rem alla -brute -reduce -q "__INPUT__" "__OUTPUT__"'
        else:
            pngcrush = 'pngcrush -rem alla -brute -reduce "__INPUT__" "__OUTPUT__"'

        # the command to execute this optimiser
        self.commands = (# pngnq seems to degrade visual quality, disable for now
                         #'pngnq -n 256 "__INPUT__"',
                         pngcrush,
                         )

        # format as returned by 'identify'
        self.format = "PNG"


#    def _get_output_file_name(self):
#        """
#        Returns the input file name with Optimiser.output_suffix inserted before the extension
#        """
#        (basename, extension) = os.path.splitext(self.input)
#
#        if extension.lower() == '.png':
#            return basename + Optimiser.output_suffix
#
#        return self.input + Optimiser.output_suffix
