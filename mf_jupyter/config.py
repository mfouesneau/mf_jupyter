import sys
import os
import inspect

mf_jupyter_path = '/'.join(os.path.abspath(inspect.getfile(inspect.currentframe())).split('/')[:-1])
sys.path.append(mf_jupyter_path)
c = get_config()

c.Exporter.filters = {
    'latex_internal_refs': 'custom_filters.latex_internal_references',
    'newline_block': 'custom_filters.newline_block',
}
