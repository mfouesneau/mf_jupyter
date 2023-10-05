""" NBCONVERT mf_jupyter configuration file """
c = get_config()

c.Exporter.filters = {
    'latex_internal_refs': 'mf_jupyter.nbconvert.custom_filters.latex_internal_references',
    'newline_block': 'mf_jupyter.nbconvert.custom_filters.newline_block',
}

# Configure tag removal - be sure to tag your cells to remove  using the
# words remove_cell to remove cells. You can also modify the code to use
# a different tag word
c.TagRemovePreprocessor.remove_cell_tags = ("hide",)
c.TagRemovePreprocessor.remove_all_outputs_tags = ('hide-output',)
c.TagRemovePreprocessor.remove_input_tags = ('hide-input',)
c.TagRemovePreprocessor.enabled = True

print(c)


print('=============== Using MF_JUPYTER configuration =================')
