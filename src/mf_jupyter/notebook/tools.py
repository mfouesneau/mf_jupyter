"""
Some tools for the notebooks
"""
from IPython.display import display, Markdown
try:
    from nbconvert.filters.markdown import markdown2latex, markdown2html
except ImportError:
    from IPython.nbconvert.filters.markdown import markdown2latex, markdown2html
from IPython.display import DisplayObject
from IPython.display import IFrame, SVG, Image
import time as _time
import sys
import os
import pkg_resources
import re


# constants
rcParams = {
    # Where to store the figures
    "figdir": os.path.curdir + '/figures',
}


def _check_figdir_exists(name: str = None):
    """ Check the directory existence or create it if needed

    Parameters
    ----------
    name : str, optional
        The name of the directory to check
    """
    if name is None:
        name = rcParams['figdir']
    if not os.path.isdir(name):
        os.makedirs(name)


def set_figures_directory(name: str):
    """ Set the figures directory

    Parameters
    ----------
    name : str
        The name of the directory to set
    """
    _check_figdir_exists(name)
    rcParams['figdir'] = name


class AutoText(Markdown):
    """ Makes generating markdown text easier to export also in tex """
    def _repr_latex_(self) -> str:
        return markdown2latex(self.data)


class Caption(Markdown):
    """ Make a caption to associate with figures """
    def __init__(self, s, center=False, **kwargs):
        Markdown.__init__(self, s, **kwargs)
        self._center = center

    def _repr_html_(self):
        """ HTML representation of the caption for the notebook"""
        txt = markdown2html(self.data)
        if self._center:
            return '<center>{0}</center>'.format(txt)
        else:
            return '{0}'.format(txt)

    def _repr_latex_(self):
        """ LaTeX representation of the caption for the exports """
        txt = markdown2latex(self.data)
        if self._center:
            return '\\begin{center}\n' + txt + '\n\\end{center}'
        else:
            return txt

    def display(self):
        """ Display the caption (`IPython.display.display`) """
        display(self)

    def __str__(self):
        """ String representation of the caption """
        return self._repr_latex_()


class Matrix(object):
    """ Make a bmatrix representation (square brackets) """
    def __init__(self,s, fmt='%0.4g'):
        self.s = s
        self._fmt = fmt

    def _repr_(self):
        """ Markdown representation of the matrix """
        text = r"""\begin{bmatrix}"""
        t = []
        for k in self.s:
            t.append( ' & '.join([self._fmt % v for v in k] ) + r'\\' )
        text += ''.join(t)
        text += r"""\end{bmatrix}"""
        return Markdown(text)

    def _repr_latex_(self):
        """ Latex representation of the matrix """
        text = r"""\begin{bmatrix}"""

        t = []
        for k in self.s:
            t.append( ' & '.join([self._fmt % v for v in k] ) + r'\\' )
        text += ''.join(t)
        text += r"""\end{bmatrix}"""
        return text

    def __str__(self):
        """ String representation of the matrix """
        return self._repr_latex_()

    def display(self):
        """ Display the object (`IPython.display.display`) """
        display(self)


def disp_markdown(*args):
    """ A shortcut to display(Markdown(*args)) """
    return display(Markdown(*args))


def load_latex_macros():
    """ Read in the latex_macro file provided with the package and display it as Markdown

    The file contains latex macro definitions that MathJax will use to render the notebook.

    Note: You may want to hide the cell from the exports to avoid redefinition of macros.
    """
    mf_nbconvert_pkg_path = os.path.abspath(pkg_resources.resource_filename('mf_jupyter', 'notebook'))
    macrofile = os.path.join(mf_nbconvert_pkg_path, 'latex_macros')
    return disp_markdown(open(macrofile).read())


def _remove_indent(txt: str) -> str:
    """ removes indents from python code string definitions """
    return re.sub(r'^\s+', '', txt,
                  flags=re.MULTILINE|re.DOTALL)


class PDF(object):
    def __init__(self,url):
        self.url = url

    def _repr_html_(self):
        return '<iframe src=%s></iframe>' % self.url

    def _repr_latex_(self):
        return r'\begin{center} \adjustimage{max size={0.9\linewidth}{0.9\paperheight}}{%s}\end{center}' % self.url


class Table(DisplayObject):
    VDOTS = object()

    def __init__(self, data, headings=None, formats=None, caption=None,
                 label=None, position='h', fontsize=None, subtables=1):
        """
        A HTML/LaTeX IPython DisplayObject Table

        `data` should be a 2 dimensional array, indexed by row then column,
        with an optional extra row `headings`.

        A 'row' (i.e., an element of `data`) may also be
        :py:const:`Table.VDOTS`, which produces vertical dots in all columns.

        `formats` may be a string, whose format method will be used for every
        cell; a function, called for every cell; or a mixed array of strings
        and functions which is zipped with each row.
        Headings are not formatted.

        `caption` and `label` add the relevant LaTeX markup, and will go in
        the first row of the HTML copy. `label` will have ``tab:`` prepended
        to it.

        If `subtables` is greater than 1, the table will be split into
        `subtables` parts of approximately equal length, and laid out side
        by side.
        """

        if len(data) == 0:
            raise ValueError("data is empty")

        if label is None != caption is None:
            raise ValueError("specify neither or both of label & caption")

        self.columns = len(data[0])
        if self.columns == 0:
            raise ValueError("no columns")

        if headings and len(headings) != self.columns:
            raise ValueError("bad headings length")

        if isinstance(formats, str):
            formats = [formats.format] * self.columns
        elif callable(formats):
            formats = [formats] * self.columns
        elif formats:
            if len(formats) != self.columns:
                raise ValueError("bad formats length")

            def maybe_string_format(f):
                if isinstance(f, str):
                    return f.format
                else:
                    assert callable(f)
                    return f

            formats = list(map(maybe_string_format, formats))
        else:
            formats = [self._default_format] * self.columns

        for i, row in enumerate(data):
            if row is not self.VDOTS and len(row) != self.columns:
                raise ValueError("bad row length", i)

        self.headings = headings
        self.data = data
        self.formats = formats
        self.caption = caption
        self.label = label
        self.position = position
        self.subtables = subtables
        self.fontsize = fontsize

    @staticmethod
    def _default_format(what):
        if isinstance(what, float):
            return "{0:.5f}".format(what)
        else:
            return str(what)

    def _format_rows(self):
        for row in self.data:
            if row is self.VDOTS:
                yield self.VDOTS
            else:
                yield (f(x) for f, x in zip(self.formats, row))

    def _subtables_split(self):
        assert self.subtables > 1

        rows = list(self._format_rows())
        nominal_height = len(rows) // self.subtables
        remainder = len(rows) % self.subtables

        heights = [nominal_height] * self.subtables
        for i in range(remainder):
            heights[i] += 1

        slices = []
        acc = 0
        for l in heights:
            slices.append((acc, acc + l))
            acc += l
        assert slices[-1][1] == len(rows)

        subtables = [rows[a:b] for a, b in slices]
        return subtables

    def _repr_latex_(self):
        strings = []

        strings.append(r"""\begin{table}""")
        if self.position not in (None, ''):
            strings.append("[" + self.position + r"]")
        strings.append("""
        \centering
        """)

        if self.label:
            strings.append(r"\caption{" + markdown2latex(self.caption) + "}")
            strings.append(r"\label{tab:" + self.label + "}")

        if self.fontsize:
            strings.append("\n" + self.fontsize + "\n")
        if self.subtables > 1:
            subtables = self._subtables_split()
            width = "{:.3f}\linewidth".format(0.95 / self.subtables)

            for i, rows in enumerate(subtables):
                strings.append(r"\begin{{subtable}}[t]{{{0}}}%".format(width))
                strings.append(r"""
                \centering
                \vspace{0pt}
                """)
                self._latex_tabular(strings, rows)
                strings.append(r"\end{subtable}%")
                if i != len(subtables) - 1:
                    strings.append("\hfill%")

        else:
            rows = self._format_rows()
            self._latex_tabular(strings, rows)

        strings.append(r"""\end{table} """)
        return "\n".join(strings)

    def _latex_tabular(self, strings, rows):
        x = "|".join(["c"] * self.columns)
        strings.append(r"\begin{tabular}{|" + x + "|}")
        strings.append(r"\hline")

        if self.headings:
            latex = " & ".join(str(x) for x in self.headings)
            strings.append(latex + r" \\")
            strings.append(r"\hline")

        for row in rows:
            if row is self.VDOTS:
                row = [r"\vdots"] * self.columns
            latex = " & ".join(row)
            strings.append(latex + r" \\")

        strings.append(r"""
        \hline
        \end{tabular}%""")

    def _repr_html_(self):
        strings = []

        strings.append("""
        <style type="text/css">
        .util_Table td { text-align: center; }
        .util_Table tbody tr, .util_Table tbody td {
            border-bottom: 0;
            border-top: 0;
        }
        .util_Table_subtable {
            float: left;
        }
        </style>
        """)

        if self.label:
            c = self.caption
            l = "<code>[{}]</code>".format(self.label)

            strings.append("""
            <h3>{1} {2}</h3>
            """.format(self.columns, c, l))

        if self.subtables > 1:
            subtables = self._subtables_split()
            # width = 0.95 / self.subtables

            strings.append("<div class='clearfix'>")
            for rows in subtables:
                strings.append("<div class='util_Table_subtable'>")
                self._html_table(strings, rows)
                strings.append("</div>")
            strings.append("</div>")

        else:
            rows = self._format_rows()
            self._html_table(strings, rows)

        return "\n".join(strings)

    def _html_table(self, strings, rows):
        strings.append("<table class='util_Table'>")

        if self.headings:
            strings.append("<thead>")
            strings.append("<tr>")
            headings = map("<th>{0}</th>".format, self.headings)
            strings.append("\n".join(headings))
            strings.append("</tr>")
            strings.append("</thead>")

        strings.append("<tbody>")

        for row in rows:
            if row is self.VDOTS:
                row = ["\u22ee"] * self.columns

            strings.append("<tr>")
            row = map("<td>{0}</td>".format, row)
            strings.append("\n".join(row))
            strings.append("</tr>")

        strings.append("</tbody>")
        strings.append("</table>")

    def __repr__(self):
        if self.headings:
            widths = [len(x) for x in self.headings]
            data = [self.headings]
        else:
            widths = None
            data = []

        # don't forget - self._format_rows() is a generator that yields generators
        for row in self._format_rows():
            if row is self.VDOTS:
                continue

            r = list(row)
            w = [len(x) for x in r]

            if widths is None:
                widths = w
            else:
                widths = [max(a, b) for a, b in zip(widths, w)]

            data.append(list(r))

        strings = []
        if self.label:
            c = self.caption.replace("\n", " ")
            strings.append('Table: {0} ({1})'.format(self.label, c))

        for row in data:
            if row is self.VDOTS:
                strings.append('...')
            else:
                r = [x.ljust(b + 4) for x, b in zip(row, widths)]
                strings.append(''.join(r))

        return '\n'.join(strings)

    def __html__(self):
        return self._repr_html_()

    def transpose(self):
        """ transpose table """
        data_ = [self.headings] + self.data
        data = list(map(list, zip(*data_)))
        return self.__class__(data)

    @property
    def T(self):
        return self.transpose()

    def set_header(self, header=None, first_row=False):
        if (not header) and (not first_row):
            return
        elif header:
            if self.columns != len(header):
                msg = "Proposed header has {0:d} fields, expecting {1:d}"
                raise AttributeError(msg.format(self.columns, len(header)))
            self.headings = header
        else:
            self.headings = self.data.pop(0)
        return self

    @classmethod
    def from_pandas(cls, df, **kwargs):
        data = df.to_records()
        headings = list(data.dtype.names)
        headings = kwargs.pop("headings", headings)
        return cls(data.tolist(), headings=headings, **kwargs)

    def _repr_jira_(self) -> str:
        """ returns the jira ascii formatted table """

        def _jira_tabular(strings: list, rows: list):

            if self.headings:
                strings.append('|| ' + " || ".join([str(x) for x in self.headings]) + ' ||')
            for row in rows:
                strings.append("| " + " | ".join(list(row)) + " |")

        strings = []

        if self.label:
            strings.append("*" + self.caption + "*")
        if self.subtables > 1:
            raise NotImplementedError()
        else:
            rows = self._format_rows()
            _jira_tabular(strings, rows)

        return "\n".join(strings)

    def to_jira(self):
        return self._repr_jira_()


class AppendixMark(Markdown):
    """ Add the appendix mark """
    def __init__(self):
        Markdown.__init__(self, '# Appendix')

    def _repr_latex_(self):
        return '\n' + r'\appendix' + '\n'


class Acknowledgements(Markdown):
    """ Set the acknowledgements section """

    def __init__(self, text, *args, **kwargs):
        self.text = text
        Markdown.__init__(self, '**acknowledgements**\n' + text)

    def _repr_latex_(self):
        return ('\n' + r'\begin{acknowledgements}' +
                '\n' + markdown2latex(self.text) +
                '\n' + r'\end{acknowledgements}')


class LatexFigure(object):
    """ Deals with figures to be properly exported in LaTeX """

    extension = 'pdf'

    def __init__(self, label, caption, fig=None, position="", star=False,
                 options='width=\columnwidth', margin=False):
        """
        A LaTeX IPython DisplayObject Figure

        `label` is mandatory, since it also sets the filename. It will
        have ``fig:`` preprended to it.

        `fig` is optional - the current figure (via ``gcf``) will be used
        if it is not set.

        `position` is either the float placement specifier or the subfigure
        vertical position.

        If `subfigure` is set to true, a subfigure with width `width` will
        be created.

        The figure is saved (via ``savefig``) as a PDF file in the current
        directory.

        Displaying the object produces LaTeX (only) to embed the figure.
        A little hacky, but since this is meant for use in the notebook
        it is assumed that the figure is going to be displayed automatically
        in HTML independently.
        """
        if fig is None:
            from matplotlib.pyplot import gcf
            fig = gcf()

        _check_figdir_exists()

        self.label = label
        self.caption = caption
        self.fig = fig
        self.position = position
        self.options = options
        self.star = star
        self.margin = margin

        self.filename = "{figdir:s}/figure_{0:s}.{1:s}"
        self.filename = self.filename.format(label, self.__class__.extension,
                                             **rcParams)

        import pylab as plt

        try:
            plt.savefig(self.filename, bbox_inches='tight')
        except:
            plt.savefig(self.filename)

    def _repr_html_(self):
        # Bit crude. Hide ourselves to the notebook viewer, since we'll
        # have been shown already anyway.
        # Nicer solutions are afaict infeasible.
        return markdown2html('> **Figure (<a name="fig:{label:s}">{label:s}</a>)**: {caption:s}'.format(
            label=self.label, caption=self.caption))

    def _repr_latex_(self, subfigure=None):
        if subfigure:
            environment = "subfigure"
            args = "[{position}]{{{width}}}".format(**subfigure)
        else:
            environment = "figure"
            args = "[{0}]".format(self.position)
        args = args.replace('[]', '')

        if self.star:
            environment += '*'
        elif self.margin & (not subfigure):
            environment = "margin" + environment

        return r"""\begin{{{env:s}}}{args:s}
            \centering
            \includegraphics[{options:s}]{{{fname:s}}}
            \caption{{{caption:s}}}
            \label{{fig:{label:s}}}
            \end{{{env:s}}}
            """.format(env=environment, args=args, options=self.options,
                       fname=self.filename, caption=markdown2latex(self.caption),
                       label=self.label)

    def __repr__(self):
        c = self.caption.replace("\n", " ")
        return "Figure: {0} ({1})".format(self.label, c)

    def __html__(self):
        return ""


class LatexMultiFigures(object):
    """ Displays several :cls:`LatexFigures` as sub-figures, two per row."""

    def __init__(self, label, caption, figures, position='',
                 rescale=True, star=False):
        """
        Displays several :cls:`LatexFigures` as sub-figures, two per row.

        `figures` should be an array of :cls:`LatexFigure` objects, not
        :cls:`matplotlib.Figure` objects.
        """

        self.label = label
        self.caption = caption
        self.figures = figures
        self.position = position
        self.star = star
        self.rescale = rescale

    def _repr_html_(self):
        # Bit crude. Hide ourselves to the notebook viewer, since we'll
        # have been shown already anyway.
        # Nicer solutions are afaict infeasible.
        return markdown2html('> **Figure (<a name="fig:{label:s}">{label:s}</a>)**: {caption:s}'.format(
            label=self.label, caption=self.caption))

    def _repr_latex_(self):
        strings = []

        environment = "figure"
        if self.star:
            environment += '*'

        strings.append(r"""\begin{""" + environment + """}[""" + self.position + r"""]
            \centering
        """)

        opts = {}
        if self.rescale is True:
            opts["width"] = "{0:0.2f}\linewidth".format((1 - len(self.figures) * 0.01) / len(self.figures))
        else:
            opts["width"] = "\columnwidth"

        for f in self.figures:
            # have to be quite careful about whitespace
            latex = r"""\includegraphics[{options:s}]{{{fname:s}}}"""
            strings.append(latex.format(options=f.options, fname=f.filename))

        strings.append(r"""
            \caption{""" + markdown2latex(self.caption) + r"""}
            \label{fig:""" + self.label + r"""}
        \end{""" + environment + """}
        """)

        return "\n".join(strings).replace('[]', '')

    def __repr__(self):
        c = self.caption.replace("\n", " ")
        strings = ["Figure group: {0} ({1})".format(self.label, c)]
        strings += [repr(x) for x in self.figures]
        return "\n".join(strings)

    def __html__(self):
        return ""


class LatexSubfigures(object):
    """ Displays several :cls:`LatexFigures` as sub-figures, two per row. """

    def __init__(self, label, caption, figures, position='h',
                 subfigure_position='b', rescale=True, star=False):
        """
        Displays several :cls:`LatexFigures` as sub-figures, two per row.

        `figures` should be an array of :cls:`LatexFigure` objects, not
        :cls:`matplotlib.Figure` objects.
        """

        self.label = label
        self.caption = caption
        self.figures = figures
        self.position = position
        self.subfigure_position = subfigure_position
        self.star = star
        self.rescale = rescale

    def _repr_html_(self):
        # Bit crude. Hide ourselves to the notebook viewer, since we'll
        # have been shown already anyway.
        # Nicer solutions are afaict infeasible.
        return markdown2html('> **Figure (<a name="fig:{label:s}">{label:s}</a>)**: {caption:s}'.format(
            label=self.label, caption=self.caption))

    def _repr_latex_(self):
        strings = []

        environment = "figure"
        if self.star:
            environment += '*'

        strings.append(r"""\begin{""" + environment + """}[""" + self.position + r"""]
            \centering
        """)

        opts = {"position": self.subfigure_position}
        if self.rescale is True:
            opts["width"] = "{0:0.2f}\linewidth".format((1 - len(self.figures) * 0.01) / len(self.figures))
        else:
            opts["width"] = "\columnwidth"

        for f in self.figures:
            # have to be quite careful about whitespace
            latex = f._repr_latex_(subfigure=opts).strip()

            strings.append(latex)

        strings.append(r"""
            \caption{""" + self.caption + r"""}
            \label{fig:""" + self.label + r"""}
        \end{""" + environment + """}
        """)

        return "\n".join(strings)

    def __repr__(self):
        c = self.caption.replace("\n", " ")
        strings = ["Figure group: {0} ({1})".format(self.label, c)]
        strings += [repr(x) for x in self.figures]
        return "\n".join(strings)

    def __html__(self):
        return ""


class LatexNumberFormatter(object):
    """
    Format floats in exponent notation using latex markup for the exponent

    e.g., ``$-4.234 \\times 10^{-5}$``

    Usage:

    >>> fmtr = LatexNumberFormatter(sf=4)
    >>> fmtr(-4.234e-5)
    "$-4.234 \\\\times 10^{-5}$"
    """

    def __init__(self, sf=10):
        """Create a callable object that formats numbers"""
        self.sf = sf
        self.s_fmt = "{{:.{0}e}}".format(self.sf)

    def __call__(self, n):
        """Format `n`"""
        n = self.s_fmt.format(n)
        n, e, exp = n.partition("e")
        if e == "e":
            exp = int(exp)
            if not n.startswith("-"):
                n = r"\phantom{-}" + n
            return r"${} \times 10^{{{}}}$".format(n, exp)
        else:
            return "${}$".format(n)


class IncludeGraphics(LatexFigure):
    """
    A LaTeX IPython DisplayObject Figure

    `label` is mandatory, since it also sets the filename. It will
    have ``fig:`` preprended to it.

    `fig` is optional - the current figure (via ``gcf``) will be used
    if it is not set.

    `position` is either the float placement specifier or the subfigure
    vertical position.

    If `subfigure` is set to true, a subfigure with width `width` will
    be created.

    The figure is saved (via ``savefig``) as a PDF file in the current
    directory.

    Displaying the object produces LaTeX (only) to embed the figure.
    A little hacky, but since this is meant for use in the notebook
    it is assumed that the figure is going to be displayed automatically
    in HTML independently.
    """
    def __init__(self, fname, label, caption, fig=None, position="", star=False,
                 options='width=\columnwidth', margin=False):
        if fig is None:
            from matplotlib.pyplot import gcf
            fig = gcf()

        self.label = label
        self.caption = caption
        self.fig = fig
        self.position = position
        self.options = options
        self.star = star
        self.margin = margin
        self.filename = fname
        self.data = self._get_data()

    def _get_data(self):
        extension = self.filename.split('.')[-1].lower()
        if extension == 'svg':
            return SVG(filename=self.filename)
        elif extension == 'pdf':
            return IFrame("mftex/pgm.pdf#view=fit", 600, 400)
        else:
            return Image(filename=self.filename)

    def _repr_html_(self):
        return markdown2html('> **Figure (<a name="fig:{label:s}">{label:s}</a>)**: {caption:s}'.format(
            label=self.label, caption=self.caption)) + '\n' + self.data._repr_html_()


class LatexMultiFigures(object):
    def __init__(self, label, caption, figures, position='',
                 rescale=True, star=False):
        """
        Displays several :cls:`LatexFigures` as sub-figures, two per row.

        `figures` should be an array of :cls:`LatexFigure` objects, not
        :cls:`matplotlib.Figure` objects.
        """

        self.label = label
        self.caption = caption
        self.figures = figures
        self.position = position
        self.star = star
        self.rescale = rescale

    def _repr_html_(self):
        # Bit crude. Hide ourselves to the notebook viewer, since we'll
        # have been shown already anyway.
        # Nicer solutions are afaict infeasible.
        return markdown2html('> **Figure (<a name="fig:{label:s}">{label:s}</a>)**: {caption:s}'.format(
            label=self.label, caption=self.caption))

    def _repr_latex_(self):
        strings = []

        environment = "figure"
        if self.star:
            environment += '*'

        strings.append(r"""\begin{""" + environment + """}[""" + self.position + r"""]
            \centering
        """)

        opts = {}
        if self.rescale is True:
            opts["width"] = "{0:0.2f}\linewidth".format((1 - len(self.figures) * 0.01) / len(self.figures))
        else:
            opts["width"] = "\columnwidth"

        for f in self.figures:
            # have to be quite careful about whitespace
            latex = r"""\includegraphics[{options:s}]{{{fname:s}}}"""
            strings.append(latex.format(options=f.options, fname=f.filename))

        strings.append(r"""
            \caption{""" + self.caption + r"""}
            \label{fig:""" + self.label + r"""}
        \end{""" + environment + """}
        """)

        return "\n".join(strings).replace('[]', '')

    def __repr__(self):
        c = self.caption.replace("\n", " ")
        strings = ["Figure group: {0} ({1})".format(self.label, c)]
        strings += [repr(x) for x in self.figures]
        return "\n".join(strings)

    def __html__(self):
        return ""