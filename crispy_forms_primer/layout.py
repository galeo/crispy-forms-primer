from django.template.loader import render_to_string

from crispy_forms import layout as crispy_forms_layout
from crispy_forms.utils import TEMPLATE_PACK, flatatt


__all__ = [
    'Layout', 'HTML', 'Div', 'DL', 'FormGroup', 'InputGroup',
    'FormActions', 'ButtonElement', 'ButtonSelectMenu',
    'Field', 'InlineCheckboxes', 'InlineRadios', 'MultiField'
]


class Layout(crispy_forms_layout.Layout):
    pass


class HTML(crispy_forms_layout.HTML):
    pass


class Div(crispy_forms_layout.Div):
    """
    It wraps fields inside a ``<div>`` element.

    You can set ``css_id`` for element id and ``css_class`` for a element
    class names.

    Example:

    .. sourcecode:: python

        Div('form_field_1', 'form_field_2', css_id='div-example',
            css_class='divs')
    """
    template = "%s/layout/div.html"


class DL(crispy_forms_layout.Div):
    """
    It wraps fields inside a ``<dl>`` element.

    Example:

    .. sourcecode:: python

        DL('form_field_1', 'form_field_2', css_id='dl-exmple',
           css_class='form-group')
    """
    template = "%s/layout/dl.html"

    def render(self, form, form_style, context, template_pack=TEMPLATE_PACK, **kwargs):
        fields = self.get_rendered_fields(form, form_style, context, template_pack, **kwargs)

        template = self.get_template_name(template_pack)
        return render_to_string(template, {'dl': self, 'fields': fields})


class FormGroup(DL):
    """
    Act like ``DL`` but add a ``form-group`` class name.
    """
    def __init__(self, field, *args, **kwargs):
        kwargs['css_class'] = kwargs.get('css_class', '') + ' form-group'
        super(InputGroup, self).__init__(field, *args, **kwargs)


class InputGroup(crispy_forms_layout.Div):
    """
    Act like ``Div`` but add a ``input-group`` class name.
    """
    def __init__(self, field, *args, **kwargs):
        kwargs['css_class'] = kwargs.get('css_class', '') + ' input-group'
        super(InputGroup, self).__init__(field, *args, **kwargs)


class FormActions(crispy_forms_layout.Div):
    """
    Act like ``Div`` but add a ``form-actions`` class name.

    Align buttons to the right—via ``float: right`` on the
    buttons—in forms with ``.form-actions``.
    The floats are automatically cleared for you.
    """
    def __init__(self, field, *args, **kwargs):
        kwargs['css_class'] = kwargs.get('css_class', '') + ' from-actions'
        super(InputGroup, self).__init__(field, *args, **kwargs)


class ButtonElement(crispy_forms_layout.BaseInput):
    """
    Contrary to ``Button``, ButtonElement purpose use a ``<button>`` element
    to create a clickable form button and accept an argument to add free
    content inside element.

    Advantage of ``<button>`` is to accept almost any HTML content inside
    element.

    .. sourcecode:: python

        button = ButtonElement('name', 'value',
                               content="<span>Press Me!</span>")

    .. note::
            * First argument is for ``name`` attribute and also turned into
              the id for the button;
            * Second argument is for ``value`` attribute and also for element
              content if not given;
            * Third argument is an optional named argument ``content``, if
              given it will be appended inside element instead of ``value``.
              Content string is marked as safe so you can put anything you
              want;
    """
    template = "%s/layout/basebutton.html"
    input_type = 'button'
    field_classes = 'btn'

    def __init__(self, field, *args, **kwargs):
        self.content = kwargs.pop('content', None)
        super(ButtonElement, self).__init__(field, *args, **kwargs)

    def render(self, form, form_style, context, template_pack=TEMPLATE_PACK):
        context['button_content'] = self.content
        return super(ButtonElement, self).render(form, form_style, context,
                                                 template_pack)


class ButtonSelectMenu(ButtonElement):
    """
    Create a ``select-menu-button`` following the ``ButtonElement`` behaviors.
    """
    input_type = 'button'
    field_classes = 'btn select-menu-button'


class Field(crispy_forms_layout.Field):
    """
    Layout object, It contains one field name, and you can add attributes to it easily.
    For setting class attributes, you need to use `css_class`, as `class` is a Python keyword.

    Example::

        Field('field_name', style="color: #333;", css_class="whatever", id="field_name")
    """
    template = "%s/field.html"


class InlineCheckboxes(Field):
    """
    Layout object for rendering checkboxes inline::

        InlineCheckboxes('field_name')
    """
    template = "%s/layout/checkboxselectmultiple_inline.html"

    def render(self, form, form_style, context, template_pack=TEMPLATE_PACK, **kwargs):
        return super(InlineCheckboxes, self).render(
            form, form_style, context, template_pack=template_pack,
            extra_context={'inline_class': 'inline'}
        )


class InlineRadios(Field):
    """
    Layout object for rendering radiobuttons inline::

        InlineRadios('field_name')
    """
    template = "%s/layout/radioselect_inline.html"

    def render(self, form, form_style, context, template_pack=TEMPLATE_PACK, **kwargs):
        return super(InlineRadios, self).render(
            form, form_style, context, template_pack=template_pack,
            extra_context={'inline_class': 'inline'}
        )


class MultiField(crispy_forms_layout.MultiField):
    """ MultiField container. Renders to a MultiField <div> """
    template = "%s/layout/multifield.html"
    field_template = "%s/multifield.html"

    def __init__(self, label, *fields, **kwargs):
        self.fields = list(fields)
        self.label_html = label
        self.label_class = kwargs.pop('label_class', '')
        self.css_class = kwargs.pop('css_class', '')
        self.css_id = kwargs.pop('css_id', None)
        self.help_text = kwargs.pop('help_text', None)
        self.template = kwargs.pop('template', self.template)
        self.field_template = kwargs.pop('field_template', self.field_template)
        self.flat_attrs = flatatt(kwargs)
