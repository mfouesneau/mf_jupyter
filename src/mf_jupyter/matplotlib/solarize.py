from copy import deepcopy
import numpy as np
import matplotlib as mpl
import pylab as plt


class Solarize(object):
    """ Namespace containing tools associated with Solarize colorscheme

    .. reference::

        http://ethanschoonover.com/solarized
    """

    COLOR = {"base03": "#002B36",
             "base02": "#073642",
             "base01": "#586e75",
             "base00": "#657b83",
             "base0": "#839496",
             "base1": "#93a1a1",
             "base2": "#eee8d5",
             "base3": "#fdf6e3",
             "yellow": "#b58900",
             "orange": "#cb4b16",
             "red": "#dc322F",
             "magenta": "#d33682",
             "violet": "#6c71c4",
             "blue": "#268bd2",
             "cyan": "#2aa198",
             "green": "#859900"
             }

    # rebase: original naming for dark, renamed for light
    DARK = {"03": COLOR["base03"],
            "02": COLOR["base02"],
            "01": COLOR["base01"],
            "00": COLOR["base00"],
            "0":  COLOR["base0"],
            "1":  COLOR["base1"],
            "2":  COLOR["base2"],
            "3":  COLOR["base3"]
            }

    LIGHT = {"03": COLOR["base3"],
             "02": COLOR["base2"],
             "01": COLOR["base1"],
             "00": COLOR["base0"],
             "0":  COLOR["base00"],
             "1":  COLOR["base01"],
             "2":  COLOR["base02"],
             "3":  COLOR["base03"]
             }

    def __init__(self, mode):
        """call :func:`Solarize.solarize`"""
        return self.__class__.solarize(mode)

    @classmethod
    def solarize(cls, mode="light"):
        """ Changes default colors of matplotlib to solarized.
        Will save the initial params that could be restored with
        the :func:`restore` method.

        Parameters
        ----------
        mode: str, optional
            Can be "light" or "dark".
        """
        if mode == "dark":
            rebase = cls.DARK
        elif mode == "light":
            rebase = cls.LIGHT

        if not hasattr(cls, '_rcstate'):
            cls._rcstate = deepcopy(plt.rcParams)

        params = {"ytick.color": rebase["0"],  # 'k'
                  "xtick.color": rebase["0"],  # 'k'
                  "text.color": rebase["0"],  # 'k'
                  "savefig.facecolor": rebase["03"],  # 'w'
                  "patch.facecolor": cls.COLOR["blue"],  # 'b'
                  "patch.edgecolor": rebase["0"],  # 'k'
                  "grid.color": rebase["0"],  # 'k'
                  "figure.edgecolor": rebase["03"],  # 'w'
                  "figure.facecolor": rebase["02"],  # '0.75'
                  # ['b', 'g', 'r', 'c', 'm', 'y', 'k']
                  "axes.color_cycle": [cls.COLOR["blue"],
                                       cls.COLOR["green"],
                                       cls.COLOR["red"],
                                       cls.COLOR["cyan"],
                                       cls.COLOR["magenta"],
                                       cls.COLOR["yellow"],
                                       rebase["0"]
                                       ],
                  "axes.edgecolor": rebase["0"],  # 'k'
                  "axes.facecolor": rebase["03"],  # 'w'
                  "axes.labelcolor": rebase["0"],  # 'k'
                  }

        mpl.rcParams.update(params)

    @classmethod
    def restore_rcParams(cls):
        """ restore the previous rcParams if exists """
        if hasattr(cls, '_rcstate'):
            plt.rcParams.update(cls._rcstate)

    @classmethod
    def gradient_cmap(cls, colors='yormvbcg', reverse=False):
        """returns a selective gradient based on given colors
        default is use all 8 colors from the theme

        Parameters
        ----------
        colors: str, optional
            A string of several char coded standard colors. "yormvbcg"
            default is to use all of the colors.

        reverse: bool, optional
            set to reverse the colormap values

        Results
        -------
        cmap: LinearSegmentedColormap instance
            colormap instance
        """
        from matplotlib.colors import LinearSegmentedColormap

        coldict = {}
        for color in ["yellow", "orange", "red", "magenta",
                      "violet", "blue", "cyan", "green"]:
            hex_str = cls.COLOR[color][1:]
            hex_r = hex_str[:2]
            hex_g = hex_str[2:4]
            hex_b = hex_str[4:6]
            num_r = int(hex_r, 16) / 255.
            num_g = int(hex_g, 16) / 255.
            num_b = int(hex_b, 16) / 255.
            coldict[color[0]] = np.array([num_r, num_g, num_b])

        num_colors = len(colors)

        num_gradients = num_colors - 1

        palettes = {"R": [], "G": [], "B": []}
        first = True
        for gdx in range(num_gradients):
            if first:
                c_f = 0
                first = False
            else:
                c_f = 1

            cur_num = 2
            palettes["R"].append(np.linspace(coldict[colors[gdx]][0],
                                             coldict[colors[gdx + 1]][0],
                                             cur_num)[c_f:])
            palettes["G"].append(np.linspace(coldict[colors[gdx]][1],
                                             coldict[colors[gdx + 1]][1],
                                             cur_num)[c_f:])
            palettes["B"].append(np.linspace(coldict[colors[gdx]][2],
                                             coldict[colors[gdx + 1]][2],
                                             cur_num)[c_f:])
        palette = np.vstack((np.concatenate(palettes["R"]),
                             np.concatenate(palettes["G"]),
                             np.concatenate(palettes["B"]))).T

        if reverse:
            s_map = LinearSegmentedColormap.from_list('solarize_r', palette[::-1])
        else:
            s_map = LinearSegmentedColormap.from_list('solarize', palette)
        return s_map

    @classmethod
    def dark(cls):
        """ Changes default colors of matplotlib to solarized dark theme. """
        cls.solarize('dark')

    @classmethod
    def light(cls):
        """Changes default colors of matplotlib to solarized light theme."""
        cls.solarize("light")

    @classmethod
    def add_cmap_to_mpl(cls, name='solarize'):
        """ add the colormap to the matplotlib library for usual use """
        from matplotlib import cm
        cmap = cls.gradient_cmap()
        cm.register_cmap(name, cmap=cmap)
        cm.__dict__[name] = cm.get_cmap(name)
        cmapr = cls.gradient_cmap(reverse=True)
        cm.register_cmap(name + '_r', cmap=cmapr)
        cm.__dict__[name + '_r'] = cm.get_cmap(name + '_r')

    def __enter__(self):
        return self.__class__

    def __exit__(self, *args, **kwargs):
        self.__class__.restore_rcParams()


Solarize.add_cmap_to_mpl()