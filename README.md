# crispy-forms-primer



## Introduction

This is a Django application to add
[django-crispy-forms](https://github.com/django-crispy-forms/django-crispy-forms)
layout objects for [Primer](https://github.com/primer/css).

⚠ This app does not include [Primer](https://github.com/primer/primer) assets, you will have
to install them yourself in your projects.

❗ This is pre-alpha software, I will be amending the initial commit for a while. You may not want to use it in production environment.

## Prerequisites

* [django-crispy-forms](https://github.com/django-crispy-forms/django-crispy-forms)

## Installation

The best way to install is by using `pip`:

```shell
$ pip install crispy-forms-primer
```

Or you could install the development version directly from GitHub:

```shell
$ pip install git+https://github.com/galeo/crispy-forms-primer
```

Add the app in `INSTALLLED_APPS` like this:

```python
INSTALLED_APPS = (
    ...
    'crispy_forms',
    'crispy_forms_primer',
    ...
)
```

Change crispy template pack settings to start using it in your forms:

```python
# Default layout to use with 'crispy_forms'
CRISPY_TEMPLATE_PACK = 'primer'
```

All other [django-crispy-forms](https://github.com/django-crispy-forms/django-crispy-forms)
settings option apply, see its documentation for more details.


## License

MIT License
