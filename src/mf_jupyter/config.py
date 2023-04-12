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

from pathlib import Path
# set a custom path for templates in 
c.TemplateExporter.extra_template_basedirs
my_templates = Path(mf_jupyter_path + '/templates').expanduser().absolute()
# add the custom path to the extra_template_basedirs
c.TemplateExporter.extra_template_basedirs = [my_templates]

print('=============== Using MF_JUPYTER configuration =================')
