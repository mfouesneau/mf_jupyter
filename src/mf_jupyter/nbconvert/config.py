""" NBCONVERT mf_jupyter configuration file """

c = get_config()

c.Exporter.filters = {
    'latex_internal_refs': 'mf_jupyter.nbconvert.custom_filters.latex_internal_references',
    'newline_block': 'mf_jupyter.nbconvert.custom_filters.newline_block',
}

print('=============== Using MF_JUPYTER configuration =================')
