from django import template
from django.template import Context, loader
from django.forms import BoundField


register = template.Library()


@register.simple_tag()
def primer_field(field, form_show_labels=True,
                 form_show_errors=True,
                 wrapper_class='',
                 label_class='',
                 **kwargs):
    """
    Renders a form field.

    Usage:

        {% primer_field form.my_field %}

    Example:

        {% primer_field form.my_field form_show_labels=False %}
    """
    if not field or not isinstance(field, BoundField):
        raise TypeError('field type error.')

    context = Context({
        'field': field,
        'form_show_errors': form_show_errors,
        'form_show_labels': form_show_labels,
        'wrapper_class': wrapper_class,
        'label_class': label_class,
        **kwargs
    })
    template = loader.get_template('primer/field.html')
    context = context.flatten()

    return template.render(context)
