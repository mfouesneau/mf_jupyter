from pylab import Formatter


class LatexFormatter(Formatter):
    """ Make Matplotlib use nice latex formatting

    Attributes
    ----------
    precision: float
        numerical precision of the mantisse

    delimiter: str
        delimiter between mantisse and exponent (do not add $ symbols for tex
        macros)

    .. code::

        cb = plt.colorbar(im, shrink=0.9, pad=0.01, extend=extend,
                          format=LatexFormatter(precision=0.2, delimiter='\cdot'))
    """
    def __init__(self, precision=2.3, fmt='g', delimiter=r'\times'):
        self.precision = precision
        self.delimiter = delimiter
        self.fmt = fmt

    def __call__(self, f, pos=None):
        float_str = ("{0:" + str(self.precision) + self.fmt + "}").format(f)
        if "e" in float_str:
            base, exponent = float_str.split("e")
            return (r"${0}{2}10^{{{1}}}$").format(base,
                                                  int(exponent),
                                                  self.delimiter)
        else:
            return float_str