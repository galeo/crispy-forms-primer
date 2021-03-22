from urllib.parse import parse_qs, urlparse, urlunparse

from django import template
from django.utils.encoding import force_str
from django.utils.http import urlencode
from django.utils.safestring import mark_safe


register = template.Library()


def url_replace_param(url, name, value):
    """Replace a GET parameter in an URL."""
    url_components = urlparse(force_str(url))

    params = parse_qs(url_components.query)

    if value is None:
        del params[name]
    else:
        params[name] = value

    return mark_safe(
        urlunparse(
            [
                url_components.scheme,
                url_components.netloc,
                url_components.path,
                url_components.params,
                urlencode(params, doseq=True),
                url_components.fragment,
            ]
        )
    )


def parse_url(url=None, extra=None):
    # parse the url
    parts = urlparse(url or "")
    params = parse_qs(parts.query)

    # append extra querystring parameters to the url.
    if extra:
        params.update(parse_qs(extra))

    # build url again.
    url = urlunparse([
        parts.scheme,
        parts.netloc,
        parts.path,
        parts.params,
        urlencode(params, doseq=True),
        parts.fragment
    ])
    return url


@register.inclusion_tag('primer/pagination/prev_next_pagination.html')
def primer_pagination(page, url=None, extra=None, parameter_name='page', **kwargs):
    current_page = page.number
    url = parse_url(url, extra)
    return {
        'primer_pagination_url': url,
        'num_pages': page.paginator.num_pages,
        'current_pages': current_page,
        'has_prev': page.has_previous(),
        'prev_num': page.previous_page_number() if page.has_previous() else '#',
        'has_next': page.has_next(),
        'next_num': page.next_page_number() if page.has_next() else '#',
        'parameter_name': parameter_name
    }


@register.inclusion_tag('primer/pagination/numbered_pagination.html')
def primer_numbered_pagination(page, **kwargs):
    """
    Render pagination for a page.

    **Tag name**::
        primer_pagination
    **Parameters**::
        page
            The page of results to show.
        url
            URL to navigate to for pagination forward and pagination back.
            :default: ``None``
        extra
            Any extra page parameters.
            :default: ``None``
        parameter_name
            Name of the paging URL parameter.
            :default: ``'page'``
    **Usage**::
        {% primer_pagination page %}
    **Example**::
        {% primer_pagination lines url="/pagination?page=1" %}
    """
    pagination_kwargs = kwargs.copy()
    pagination_kwargs['page'] = page
    return get_pagination_context(**pagination_kwargs)


@register.simple_tag
def primer_url_replace_param(url, name, value):
    return url_replace_param(url, name, value)


def get_pagination_context(page, url=None,  # noqa C901
                           extra=None,
                           parameter_name='page',
                           left_edge=2, left_current=2,
                           right_current=2, right_edge=2,
                           boundary=5):
    """Generate Primer pagination context from a page object."""

    def iter_pages(num_pages, current_page,
                   left_edge=2, left_current=2,
                   right_current=2, right_edge=2,
                   boundary=5):
        last = 0
        for num in range(1, num_pages + 1):
            if (
                num <= left_edge
                or (
                    num >= current_page - left_current
                    and num < current_page + right_current + 1
                )
                or num > num_pages - right_edge
            ):
                if last + 1 != num:
                    # a ... c , replace ... with b
                    if num - last == 2:
                        yield last + 1
                    else:
                        # right gap
                        if num_pages - num == 1:
                            while last < boundary:
                                yield last + 1
                                last += 1
                            gap = num - last
                            if gap == 2:
                                yield last + 1
                            if gap > 2:
                                yield '...'
                        # left gap
                        if last == left_edge:
                            delta = boundary - (num_pages - num + 1)
                            gap = num - delta - last
                            if gap == 2:
                                yield last + 1
                            if gap > 2:
                                yield '...'
                            while delta > 0:
                                yield num - delta
                                delta -= 1

                yield num
                last = num

    num_pages = page.paginator.num_pages
    current_page = page.number

    url = parse_url(url, extra)
    has_prev = current_page > 1
    prev_num = current_page - 1 if has_prev else '#'
    has_next = current_page < num_pages
    next_num = current_page + 1 if has_next else '#'
    pages = iter_pages(num_pages, current_page,
                       left_edge, left_current,
                       right_current, right_edge,
                       boundary)

    # Set CSS classes, see https://primer.style/css/components/pagination
    pagination_css_classes = ['pagination']

    return {
        'primer_pagination_url': url,
        'num_pages': num_pages,
        'current_page': current_page,
        'has_prev': has_prev,
        'prev_num': prev_num,
        'pages': pages,
        'has_next': has_next,
        'next_num': next_num,
        'pagination_css_classes': ' '.join(pagination_css_classes),
        'parameter_name': parameter_name,
    }
