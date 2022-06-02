import re
import urllib
from math import floor

from django.forms import BaseForm
from django.forms.forms import BoundField
from django.forms.widgets import TextInput, CheckboxInput, CheckboxSelectMultiple, RadioSelect
from django.template import Context
from django.template.loader import get_template
from django import template
from django.conf import settings
from django.utils.safestring import mark_safe
from django.utils.html import escape

register = template.Library()

@register.filter
def tud_breadcrumb(url):
    home = ['<li><a href="/" title="Breadcrumb link to the homepage.">home</a></li>',]
    links = url.strip('/').split('/')
    bread = []
    total = len(links)-1
    for i, link in enumerate(links):
        if not link == '':
            bread.append(link)
            this_url = "/".join(bread)
            sub_link = re.sub('-', ' ', link)
            if not i == total:
                tlink = '<li><a href="/%s/" title="Breadcrumb link to %s">%s</a></li>' % (this_url, sub_link, sub_link)
            else:
                tlink = '<li>%s</li>' % sub_link
            home.append(tlink)
    bcrumb = "".join(home)
    return get_template("tud_styling/tags/breadcrumb.html").render(
		Context({
			'html': mark_safe(bcrumb)
		})
	)

@register.simple_tag(takes_context=True)
def tud_messages(context, *args, **kwargs):
    """
    Show request messages in TU Delft Styling style
    """
    return get_template("tud_styling/tags/messages.html").render(context)
















@register.filter
def as_tud(form_or_field, layout='vertical,false'):
    """
    Render a field or a form according to TU Delft Styling guidelines
    """
    params = split(layout, ",")
    layout = str(params[0]).lower()

    try:
        tud_float = str(params[1]).lower() == "float"
    except IndexError:
        tud_float = False

    if isinstance(form_or_field, BaseForm):
        return get_template("tud_styling/tags/form.html").render(
            {
                'form': form_or_field,
                'layout': layout,
                'float': tud_float,
            }
        )
    elif isinstance(form_or_field, BoundField):
        return get_template("tud_styling/tags/field.html").render(
            {
                'field': form_or_field,
                'layout': layout,
                'float': tud_float,
            }
        )
    else:
        # Display the default
        return settings.TEMPLATE_STRING_IF_INVALID


@register.filter
def is_disabled(field):
    """
    Returns True if fields is disabled, readonly or not marked as editable, False otherwise
    """
    if not getattr(field.field, 'editable', True):
        return True
    if getattr(field.field.widget.attrs, 'readonly', False):
        return True
    if getattr(field.field.widget.attrs, 'disabled', False):
        return True
    return False


@register.filter
def is_enabled(field):
    """
    Shortcut to return the logical negative of is_disabled
    """
    return not is_disabled(field)


@register.filter
def tud_input_type(field):
    """
    Return input type to use for field
    """
    try:
        widget = field.field.widget
    except:
        raise ValueError("Expected a Field, got a %s" % type(field))
    input_type = getattr(widget, 'tud_input_type', None)
    if input_type:
        return unicode(input_type)
    if isinstance(widget, TextInput):
        return u'text'
    if isinstance(widget, CheckboxInput):
        return u'checkbox'
    if isinstance(widget, CheckboxSelectMultiple):
        return u'multicheckbox'
    if isinstance(widget, RadioSelect):
        return u'radioset'
    return u'default'


@register.simple_tag
def active_url(request, url, output=u'active'):
    # Tag that outputs text if the given url is active for the request
    if url == request.path:
        return output
    return ''


@register.filter
def pagination(page, pages_to_show=11):
    """
    Generate TU Delft Styling pagination links from a page object
    """
    context = get_pagination_context(page, pages_to_show)
#    return get_template("tud_styling/tags/pagination.html").render(Context(context))
    return get_template("tud_styling/tags/pagination.html").render(context)
#    return get_template("tud_styling/tags/pagination.html").render(Context())


@register.filter
def split(text, splitter):
    """
    Split a string
    """
    return text.split(splitter)


@register.filter
def html_attrs(attrs):
    """
    Display the attributes given as html attributes :
    >>> import collections
    >>> html_attrs(collections.OrderedDict([('href',"http://theurl.com/img.png"), ('alt','hi "guy')]))
    u'href="http://theurl.com/img.png" alt="hi &quot;guy" '
    """
    pairs = []
    for name, value in attrs.items():
        pairs.append(u'%s="%s"' % (escape(name), escape(value)))
    return mark_safe(u' '.join(pairs))


@register.simple_tag(takes_context=True)
def tud_messages(context, *args, **kwargs):
    """
    Show request messages in TU Delft Styling style
    """
#    return get_template("tud_styling/tags/messages.html").render(context)
#    return = context.template.engine.get_template("tud_styling/tags/messages.html")
    template = context.template.engine.get_template("tud_styling/tags/messages.html")
    return template.render(context)
    



@register.inclusion_tag('tud_styling/tags/social_media_sharing.html')
def social_media_sharing(data, curr_url, **kwargs):
    """
    Render a social media sharing links
    """
    curr_url = urllib.quote(curr_url)
    data2 = []
    for item in data:
        if item['type'] == 'facebook':
	        item['link'] = '//www.facebook.com/sharer/sharer.php?u=' + curr_url
        elif item['type'] == 'twitter':
	        item['link']  = '//twitter.com/share?url=' + curr_url + '&text=' + urllib.quote_plus(item['title']);
        elif item['type'] == 'linkedin':
	        item['link'] = '//www.linkedin.com/shareArticle?mini=true&url=' + curr_url + '&title=' + urllib.quote_plus(item['title']) + '&summary=' + urllib.quote_plus(item['description']) + '&source=tudelft.nl'
        data2.append(item)
    return {'data':data2}


@register.inclusion_tag("tud_styling/tags/form.html")
def tud_form(form, **kwargs):
    """
    Render a form
    """
    context = kwargs.copy()
    context['form'] = form
    return context


@register.inclusion_tag("tud_styling/tags/formset.html")
def tud_formset(formset, **kwargs):
    """
    Render a formset
    """
    context = kwargs.copy()
    context['formset'] = formset
    return context


@register.inclusion_tag("tud_styling/tags/field.html")
def tud_field(field, **kwargs):
    """
    Render a field
    """
    context = kwargs.copy()
    context['field'] = field
    return context


@register.inclusion_tag("tud_styling/tags/button.html")
def tud_button(text, **kwargs):
    """
    Render a button
    """
    button_type = kwargs.get('type', '')
    button_size = kwargs.get('size', '')
    button_disabled = kwargs.get('disabled', False) and kwargs.get('enabled', True)
    button_icon = kwargs.get('icon', '')

    # Build button classes
    button_class = 'btn'
    if button_type:
        button_class += ' btn-' + button_type
    if button_size:
        button_class += ' btn-' + button_size
    if button_disabled:
        button_class += ' disabled'
        # Build icon classes
    icon_class = ''
    if button_icon:
        icon_class = 'icon-' + button_icon
        if button_type and button_type != 'link':
            icon_class += ' icon-white'
            # Return context for template
    return {
        'text': text,
        'url': kwargs.get('url', '#'),
        'button_class': button_class,
        'icon_class': icon_class,
    }


@register.inclusion_tag("tud_styling/tags/icon.html")
def tud_icon(icon, **kwargs):
    """
    Render an icon
    """
    icon_class = 'icon-' + icon
    if kwargs.get('inverse'):
        icon_class += ' icon-white'
    return {
        'icon_class': icon_class,
    }


@register.inclusion_tag("tud_styling/tags/pagination.html")
def tud_pagination(page, **kwargs):
    """
    Render pagination for a page
    """
    pagination_kwargs = kwargs.copy()
    pagination_kwargs['page'] = page
    return get_pagination_context(**pagination_kwargs)


def get_pagination_context(page, pages_to_show=11, url=None, size=None, align=None, extra=None):
    """
    Generate TU Delft Styling pagination context from a page object
    """
    pages_to_show = int(pages_to_show)
    if pages_to_show < 1:
        raise ValueError("Pagination pages_to_show should be a positive integer, you specified %s" % pages_to_show)
    num_pages = page.paginator.num_pages
    current_page = page.number
    half_page_num = int(floor(pages_to_show / 2)) - 1
    if half_page_num < 0:
        half_page_num = 0
    first_page = current_page - half_page_num
    if first_page <= 1:
        first_page = 1
    if first_page > 1:
        pages_back = first_page - half_page_num
        if pages_back < 1:
            pages_back = 1
    else:
        pages_back = None
    last_page = first_page + pages_to_show - 1
    if pages_back is None:
        last_page += 1
    if last_page > num_pages:
        last_page = num_pages
    if last_page < num_pages:
        pages_forward = last_page + half_page_num
        if pages_forward > num_pages:
            pages_forward = num_pages
    else:
        pages_forward = None
        if first_page > 1:
            first_page -= 1
        if pages_back > 1:
            pages_back -= 1
        else:
            pages_back = None
    pages_shown = []
    for i in range(first_page, last_page + 1):
        pages_shown.append(i)
    # Append proper character to url
    if url:
        # Remove existing page GET parameters
        url = unicode(url)
        url = re.sub(r'\?page\=[^\&]+', u'?', url)
        url = re.sub(r'\&page\=[^\&]+', u'', url)
        # Append proper separator
        if u'?' in url:
            url += u'&'
        else:
            url += u'?'
    # Append extra string to url
    if extra:
        if not url:
            url = u'?'
        url += unicode(extra) + u'&'
    if url:
        url = url.replace(u'?&', u'?')
    pagination_css_classes = ['pagination']
    if size in ['small', 'large', 'mini']:
        pagination_css_classes.append('pagination-%s' % size)
    if align == 'center':
        pagination_css_classes.append('pagination-centered')
    elif align == 'right':
        pagination_css_classes.append('pagination-right')
    # Build context object
    return {
        'tud_pagination_url': url,
        'num_pages': num_pages,
        'current_page': current_page,
        'first_page': first_page,
        'last_page': last_page,
        'pages_shown': pages_shown,
        'pages_back': pages_back,
        'pages_forward': pages_forward,
        'pagination_css_classes': ' '.join(pagination_css_classes),
    }
