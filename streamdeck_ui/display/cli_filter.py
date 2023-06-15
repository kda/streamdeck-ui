import os
import importlib.util

from fractions import Fraction
from typing import Callable, Tuple

from PIL import Image

from streamdeck_ui.display import filter


class CliFilter(filter.Filter):
    """
    This is the CLI filter which adjusts the image based result of command line.

    :param str name: The name of the filter. The name is useful for debugging purposes.
    """

    def __init__(self, args: list[str]):
        super(CliFilter, self).__init__()
        self.args_ = args
        print(self.args_)

    def initialize(self, size: Tuple[int, int]):
        self.image = Image.new("RGB", size)
        spec = importlib.util.spec_from_file_location("junk", self.args_[0])
        self.mod_ = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.mod_)


    def transform(self, get_input: Callable[[], Image.Image], get_output: Callable[[int], Image.Image], input_changed: bool, time: Fraction) -> Tuple[Image.Image, int]:
        """
        Returns an empty Image object.

        :param Fraction time: The current time in seconds, expressed as a fractional number since
        the start of the pipeline.
        """
        #inputfp = tempfile.TemporaryFile()
        #print('inputfp.name: %s' % (inputfp.name))


        input_image = get_input()
        (self.image, hashcode) = self.mod_.prepareImage(input_image, self.args_[1:])

        #if not input_changed:
        #    return (None, hashcode)
        return ((self.image), hashcode)
