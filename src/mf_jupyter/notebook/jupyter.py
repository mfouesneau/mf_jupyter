""" Some jupyter notebook tools

Notes:

```python
from IPython import get_ipython
get_ipython().run_line_magic('tag', 'testing')
```
"""
from IPython.display import Javascript, display, HTML
from IPython.core.magic import register_cell_magic, register_line_cell_magic
import json

class InvisibleJavascript(Javascript):
    """ A class that removes representations """
    def __init__(self, *args, **kwargs):
        super(InvisibleJavascript, self).__init__(*args, **kwargs)

    def _repr_latex_(self):
        return ''

    def __str__(self):
        return ''

    def __repr__(self):
        return ''



def register_magic():
    """ Add magic function tag, hide, and abstract to the kernel. """

    display(InvisibleJavascript("""
    define('setTags', function() {
        return function(element, tags) {
            var cell_element = element.parents('.cell');
            var index = Jupyter.notebook.get_cell_elements().index(cell_element);
            var cell = Jupyter.notebook.get_cell(index);
            cell.metadata.tags = tags;
        }
    });

    define('setAbstract', function() {
        return function(element) {
            var cell_element = element.parents('.cell');
            var index = Jupyter.notebook.get_cell_elements().index(cell_element);
            var cell = Jupyter.notebook.get_cell(index);
            cell.metadata.abstract = "true";
        }
    });

    define('setHide', function() {
        return function(element, tags) {
            var cell_element = element.parents('.cell');
            var index = Jupyter.notebook.get_cell_elements().index(cell_element);
            var cell = Jupyter.notebook.get_cell(index);
            cell.metadata.hide = tags;
        }
    });
    """))

    def _set_tags(tags):
        assert all(map(lambda t: isinstance(t, str), tags))
        display(InvisibleJavascript(
            """
            require(['setTags'], function(setTags) {
                setTags(element, %s);
            });
            """ % json.dumps(tags)
        ))

    def _set_hide(tags):
        assert all(map(lambda t: isinstance(t, str), tags))
        display(InvisibleJavascript(
            """
            require(['setHide'], function(setHide) {
                setHide(element, %s);
            });
            """ % json.dumps(tags)
        ))

    def _set_abstract():
        display(InvisibleJavascript(
            """
            require(['setAbstract'], function(setAbstract) {
                setAbstract(element);
            });
            """
        ))

    @register_line_cell_magic
    def tag(line, cell=None):
        _set_tags(line.split())

    @register_line_cell_magic
    def hide(line, cell=None):
        _set_hide(line.split()[0])

    @register_line_cell_magic
    def abstract(line, cell=None):
        _set_abstract()


def display_toolbar():
    """ Programmatically display the mf_jupyter toolbar. """
    from IPython.display import Javascript

    display(InvisibleJavascript("""
        IPython.CellToolbar.activate_preset("mf_jupyter");
        IPython.CellToolbar.global_show();
    """))


def add_input_toggle() -> HTML:
    """ Add a button to toggle visibility of all input cells.

    You can hide input codes throughout the notebook by clicking on the button.
    """
    r = HTML('''
    <script>

    $( document ).ready(function () {
        IPython.CodeCell.options_default['cm_config']['lineWrapping'] = true;
        IPython.notebook.get_selected_cell()

        IPython.toolbar.add_buttons_group([
                {
                    'label'   : 'toggle all input cells',
                    'icon'    : 'fa-eye-slash',
                    'callback': function(){ $('div.input').slideToggle(); }
                }
            ]);
    });
    </script>
    ''')
    display(r)
    return r


def add_hide_button():
    """ Add buttom to the mf_jupyter toolbar to toggle the hide field. """
    from IPython.display import HTML, display

    r = HTML('''
             <script>
             var CellToolbar = Jupyter.CellToolbar
var mf_hide_toggle =  function(div, cell) {
     var button_container = $(div)

     // let's create a button that shows the current value of the metadata
     var button = $('<button/>').addClass('btn btn-default btn-xs').text("hide: "  + String(cell.metadata.hide));

     // On click, change the metadata value and update the button label
     button.click(function(){
                 var v = cell.metadata.hide;
                 cell.metadata.hide = !v;
                 button.text("hide: "  + String(!v));
             })

     // add the button to the DOM div.
     button_container.append(button);
}

// now we register the callback under the name foo to give the
// user the ability to use it later
CellToolbar.register_callback('mf_hide', mf_hide_toggle);

// Now we declare the toolbar
console.log('Clear mf_jupyter if exists.')
Jupyter.CellToolbar.unregister_preset('mf_jupyter')
Jupyter.CellToolbar.register_preset('mf_jupyter',['mf_hide','default.rawedit'])
console.log('Loaded extension mf_jupyter.')
             </script>
             ''')
    display(r)
    return r


def add_citation_button():
    """ Add citation button to the main notebook toolbar. """
    from IPython.display import HTML, display
    r = HTML("""
    <script>

    function insert_citn() {
        // Build paragraphs of cell type and count

        var entry_box = $('<input type="text"/>');
        var body = $('<div><p> Enter the Bibtex reference to insert </p><form>').append(entry_box)
                    .append('</form></div>');

        // Show a modal dialog with the stats
        IPython.dialog.modal({
            notebook: IPython.notebook,
            keyboard_manager: IPython.notebook.keyboard_manager,
            title: "Bibtex reference insertion",
            body: body,
            open: function() {
                // Submit on pressing enter
                var that = $(this);
                that.find('form').submit(function () {
                    that.find('.btn-primary').first().click();
                    return false;
                });
                entry_box.focus();
            },
            buttons : {
                "Cancel" : {},
                "Insert" : {
                    "class" : "btn-primary",
                    "click" : function() {
                        // Retrieve the selected citation, add to metadata,
                        var citation = entry_box.val();
                        // if (!citation) {return;}
                        var citn_html = '<cite data-cite="' + citation + '">' + citation + '</cite>';
                        var cell = IPython.notebook.get_selected_cell();
                        cell.code_mirror.replaceSelection(citn_html);
                    }
                }
            }
        });
    };

    $( document ).ready(function () {

        IPython.toolbar.add_buttons_group([
                {
                    'label'   : 'insert bibtex reference in markdown',
                    'icon'    : 'fa-graduation-cap', // http://fontawesome.io/icons/
                    'callback': insert_citn,
                }
            ]);
    });

    </script>
    <style>
    cite {
        font-style: normal;
        color: #45749e;
    }
    </style>
    """)
    display(r)
    return r
