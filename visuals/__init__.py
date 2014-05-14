from abc import ABCMeta, abstractmethod

class Visual:
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_verts(self, w, h, freqs):
        """ returns a tuple of verts, colors """
        return

from visuals.bars import Bars

visuals = {
        'bars' : Bars
}
