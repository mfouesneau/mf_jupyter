from . ipython_notebook import *
from . import (figrc, setup_mpl)


def get_package_path():
    import os
    import inspect

    mf_jupyter_path = '/'.join(os.path.abspath(inspect.getfile(inspect.currentframe())).split('/')[:-1])
    return mf_jupyter_path



