"""
Settings
========

Default required settings. You can override them in your project settings file.
"""

# Allowed layout pack
CRISPY_ALLOWED_TEMPLATE_PACKS = (
    'bootstrap',
    'uni_form',
    'bootstrap3',
    'bootstrap4',
    'primer'
)


# Default layout pack
CRISPY_TEMPLATE_PACK = 'primer'

# Default class names on input
CRISPY_CLASS_CONVERTERS = {
    'textinput': 'form-control',
    'inputelement': 'form-control',
    'numberinput': 'form-control',
    'errorcondition': 'errored',
}
