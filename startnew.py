#!/usr/bin/env python
import os
import inspect
from shutil import copyfile
from optparse import OptionParser, OptionGroup


_files_ = [
    "Makefile",
    "Untitled.ipynb",
    "bibliography.bib",
    "document_configuration.tex",
    "mf.sty"
]


def make_parser_from_options(*args, **kwargs):
    """
    Parameters
    ----------
    args: (name, options) tuples
        name of the section and options associated

    kwargs: dict
        forwarded to :class:`OptionParser`

    Returns
    -------
    parser: OptionParser instance
        parser
    """
    parser = OptionParser(**kwargs)
    for name, opt in args:
        group = OptionGroup(parser, name)
        for ko in opt:
            group.add_option(*ko[:-1], **ko[-1])
        parser.add_option_group(group)
    return parser


if __name__ == '__main__':
    curdir = os.path.curdir

    opts = dict(
        defaults=(
            ('-o', '--output', dict(dest="output", default=curdir, type='str', help="where to start a new project", metavar='FILE')),
        ),
    )
    usage_msg = """Usage: python startnew.py [options] """
    parser = make_parser_from_options(*list((k, opts[k]) for k in opts.keys()), usage=usage_msg)
    (options, args) = parser.parse_args()

    output = options.__dict__.get("output", curdir)
    mf_jupyter_path = '/'.join(os.path.abspath(inspect.getfile(inspect.currentframe())).split('/')[:-1])

    # copy necessary files
    for fname in _files_:
        copyfile("{0:s}/{1:s}".format(mf_jupyter_path, fname),
                 "{0:s}/{1:s}".format(output, fname))

    print("Project created in {0:s}".format(output))
