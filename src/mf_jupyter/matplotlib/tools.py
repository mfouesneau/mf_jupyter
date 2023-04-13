import pylab as plt
import matplotlib as mpl


def colorify(data, vmin=None, vmax=None, cmap=plt.cm.Spectral):
    """ Associate a color map to a quantity vector

    Parameters
    ----------
    data: sequence
        values to encode
    vmin: float
        minimum value
    vmax: float
        maximum value
    cmap: Colormap instance
        colormap to use

    Returns
    -------
    colors: sequence or array
        one color per input data
    cmap: Colormap
        data normalized colormap instance
    """
    try:
        from matplotlib.colors import Normalize
    except ImportError:
        # old mpl
        from matplotlib.colors import normalize as Normalize

    _vmin = vmin or min(data)
    _vmax = vmax or max(data)
    cNorm = Normalize(vmin=_vmin, vmax=_vmax)

    scalarMap = plt.cm.ScalarMappable(norm=cNorm, cmap=cmap)
    try:
        colors = scalarMap.to_rgba(data)
    except:
        colors = list(map(scalarMap.to_rgba, data))
    scalarMap.set_array(data)
    return colors, scalarMap


def create_common_cbar(vmin=0, vmax=1, box=None, **kwargs):
    """ Create a common colorbar to a complex figure

    Parameters
    ----------
    vmin: float
        minimum value on the colorscale
    vmax: float
        maximum value on the colorscale
    box: tuple
        axis definition box

    Returns
    -------
    cb: ColorBar instance
        the colorbar object
    """
    if box is None:
        box = [0.3, 0.1, 0.6, 0.02]

    kw = dict(spacing='proportional', orientation='horizontal',
              cmap=plt.cm.jet)

    kw.update(**kwargs)
    norm = kw.pop('norm', None)
    if norm is None:
        norm = mpl.colors.Normalize(vmin=vmin, vmax=vmax)

    ax = plt.gcf().add_axes(box)
    cb = mpl.colorbar.ColorbarBase(ax, norm=norm, **kw)
    return cb