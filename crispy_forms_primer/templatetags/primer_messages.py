from django import template
from django.contrib.messages import constants as message_constants
from django.template import Context
from django.template.loader import get_template


MESSAGE_LEVEL_CLASSES = {
    message_constants.DEBUG: 'flash-warn',
    message_constants.INFO: '',
    message_constants.SUCCESS: 'flash-success',
    message_constants.WARNING: 'flash-warn',
    message_constants.ERROR: 'flash-error',
}

register = template.Library()


@register.filter
def primer_message_classes(message):
    """Return the message classes for a message."""
    extra_tags = None
    try:
        extra_tags = message.extra_tags
    except AttributeError:
        pass
    if not extra_tags:
        extra_tags = ''
    classes = [extra_tags]
    try:
        level = message.level
    except AttributeError:
        pass
    else:
        try:
            classes.append(MESSAGE_LEVEL_CLASSES[level])
        except KeyError:
            classes.append('flash-error')
    return ' '.join(classes).strip()


@register.simple_tag(takes_context=True)
def primer_messages(context, *args, **kwargs):
    """
    Show django.contrib.messages Messages fully in primer alerts containers.

    Uses the template ``primer/messages.html``.

    **Tag name**::

        primer_messages

    **Parameters**:

        None.

    **Usage**::

        {% primer_messages %}

    **Example**::

        {% primer_messages extra_tags='border-0' %}
    """
    # Force Context to dict
    if isinstance(context, Context):
        context = context.flatten()
    context.update({
        'message_constants': message_constants,
        'mesage_extra_tags': kwargs.get('extra_tags')
    })
    template = get_template('primer/messages.html')
    return template.render(context)
