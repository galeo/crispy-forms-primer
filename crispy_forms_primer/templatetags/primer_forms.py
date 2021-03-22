from django import template
from django.conf import settings
from django.template import Context, loader

from crispy_forms.templatetags.crispy_forms_field import (
    pairwise, CrispyFieldNode
)
from crispy_forms.utils import get_template_pack

register = template.Library()


class CrispyPrimerFieldNode(CrispyFieldNode):
    def __init__(self, field, attrs):
        self.field = field
        self.attrs = attrs
        self.html5_required = 'html5_required'

    def render(self, context):  # noqa C901
        # Nodes are not threadsafe so we must store and look up our instance
        # variables in the current rendering context first
        if self not in context.render_context:
            context.render_context[self] = (
                template.Variable(self.field),
                self.attrs,
                template.Variable(self.html5_required)
            )

        field, attrs, html5_required = context.render_context[self]
        field = field.resolve(context)
        try:
            html5_required = html5_required.resolve(context)
        except template.VariableDoesNotExist:
            html5_required = False

        widgets = getattr(field.field.widget, 'widgets', [field.field.widget])

        if isinstance(attrs, dict):
            attrs = [attrs] * len(widgets)

        converters = {
            'textinput': 'form-control',
            'inputelement': 'form-control',
            'numberinput': 'form-control',
        }

        converters.update(getattr(settings, 'CRISPY_CLASS_CONVERTERS', {}))

        for widget, attr in zip(widgets, attrs):
            class_name = widget.__class__.__name__.lower()
            class_name = converters.get(class_name, class_name)
            css_class = widget.attrs.get('class', '')
            if css_class:
                if css_class.find(class_name) == -1:
                    css_class += " %s" % class_name
            else:
                css_class = class_name

            widget.attrs['class'] = css_class

            # HTML5 required attribute
            if html5_required and field.field.required and 'required' not in widget.attrs:
                if field.field.widget.__class__.__name__ != 'RadioSelect':
                    widget.attrs['required'] = 'required'

            for attribute_name, attribute in attr.items():
                attribute_name = template.Variable(attribute_name).resolve(context)

                if attribute_name in widget.attrs:
                    widget.attrs[attribute_name] += " " + template.Variable(attribute).resolve(context)
                else:
                    widget.attrs[attribute_name] = template.Variable(attribute).resolve(context)

        return field


@register.tag(name='crispy_field')
def crispy_field(parser, token):
    """
    {% crispy_field field attrs %}
    """
    token = token.split_contents()
    field = token.pop(1)
    attrs = {}

    # We need to pop tag name, or pairwise would fail
    token.pop(0)
    for attribute_name, value in pairwise(token):
        attrs[attribute_name] = value

    return CrispyPrimerFieldNode(field, attrs)


@register.simple_tag()
def crispy_addon(field, append="", prepend="", form_show_labels=True):
    """
    Renders a form field using primer's prepended or appended button::

        {% crispy_addon form.my_field prepend="$" append=".00" %}

    You can also just prepend or append like so

        {% crispy_addon form.my_field prepend="$" %}
        {% crispy_addon form.my_field append=".00" %}
    """
    if field:
        context = Context({
            'field': field,
            'form_show_errors': True,
            'form_show_labels': form_show_labels,
        })
        template = loader.get_template(
            '%s/layout/prepended_appended_button.html' % get_template_pack())
        context['crispy_prepended_button'] = prepend
        context['crispy_appended_button'] = append

        if not prepend and not append:
            raise TypeError("Expected a prepend and/or append argument")

        context = context.flatten()

    return template.render(context)
