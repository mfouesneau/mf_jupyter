"""Custom filters to be used with IPython nbconvert."""
import re


def newline_block(text):
    """ Filter that makes sure that a block will always start with a newline """
    return r"""
{0:s}
""".format(text)


def latex_internal_references(text):
    """Take markdown text and replace instances of
    '[blah](#anchor-ref)' with 'autoref{anchor-ref}'
    """
    ref_pattern = re.compile(r'\[(?P<text>.*?)\]\(#(?P<reference>.*?)\)')
    replacement = r'\\autoref{\g<reference>}'

    return ref_pattern.sub(replacement, text)
