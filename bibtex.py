#!/usr/bin/env python
"""
Get Bibtex entry from ads directly with bibcode

.. code::

    > python bibtex.py  "2000A&A...355L..27H" -k Hog2000
    Interrogating http://cdsads.u-strasbg.fr...
    Request: 2000A&A...355L..27H... done.
    Reading content...done.

    @ARTICLE{Hog2000,
    author = {{H{\o}g}, E. and {Fabricius}, C. and {Makarov}, V.~V. and {Urban}, S. and
            {Corbin}, T. and {Wycoff}, G. and {Bastian}, U. and {Schwekendiek}, P. and
            {Wicenec}, A.},
        title = "{The Tycho-2 catalogue of the 2.5 million brightest stars}",
    journal = {\aap},
    keywords = {ASTROMETRY, STARS: FUNDAMENTAL PARAMETERS, CATALOGS},
        year = 2000,
        month = mar,
    volume = 355,
        pages = {L27-L30},
    adsurl = {http://cdsads.u-strasbg.fr/abs/2000A%26A...355L..27H},
    adsnote = {Provided by the SAO/NASA Astrophysics Data System}
    }

:version: 1.0
:author: MF
"""
from __future__ import print_function, unicode_literals, division

import sys

if sys.version_info[0] > 2:
    py3k = True
    from urllib import request
    from urllib.request import urlopen
else:
    py3k = False
    from urllib2 import urlopen

from optparse import OptionParser, OptionGroup


adsserver = "http://cdsads.u-strasbg.fr"
url = "{adsserver:s}/cgi-bin/nph-bib_query?bibcode={bibcode:s}&data_type=BIBTEX&db_key=AST&nocookieset=1"


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


def get_bibentry(bibcode="2000A&A...355L..27H"):

    print('Interrogating {adsserver:s}...'.format(adsserver=adsserver))

    print('Request: {bibcode:s}... '.format(bibcode=bibcode), end='')
    if py3k:
        req = request.Request(url.format(adsserver=adsserver, bibcode=bibcode))
        print('done.')
        print("Reading content...", end='')
        c = urlopen(req).read().decode('utf8')
    else:
        c = urlopen(url.format(adsserver=adsserver, bibcode=bibcode))

    c = '@' + c.split('@')[-1]  # get rid of anything above @ARTICLE etc
    print('done.')
    return c


if __name__ == "__main__":

    opts = dict(
        defaults=(
            ('-o', '--output', dict(dest="output", default='-', type='str', help="Add entry to this file", metavar='FILE')),
            ('-k', '--bibkey', dict(dest="bibkey", default="", type='str', help="Bibkey")),
        ),
    )

    usage_msg = """
    usage: python bibtex.py [options] bibcode """

    parser = make_parser_from_options(*list((k, opts[k]) for k in opts.keys()), usage=usage_msg)

    (options, args) = parser.parse_args()

    try:
        c = get_bibentry(args[0])
        key = options.__dict__.get("bibkey", args[0])
    except IndexError:
        print("wrong number of arguments. --help for details" + usage_msg)
        sys.exit(1)

    if key not in (None, "None", ""):
        c = c.replace(args[0], key)

    output = options.__dict__.get("output", '-')
    if output in (None, "None", "-", ""):
        print(c)
    else:
        print("Writing Bibentry to {0:s}".format(output))
        with open(output, "a") as f:
            f.write("\n")
            f.write(c)
