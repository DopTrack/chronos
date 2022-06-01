from django import forms
from django.conf import settings
from django.utils import translation
from django.utils.safestring import mark_safe
from django.utils.html import conditional_escape
from django.contrib.staticfiles import finders


default_date_format = getattr(settings, 'DATE_INPUT_FORMATS', None)
if default_date_format:
    default_date_format = str(default_date_format[0])


def javascript_date_format(python_date_format):
    js_date_format = python_date_format.replace(r'%Y', 'yyyy')
    js_date_format = js_date_format.replace(r'%m', 'mm')
    js_date_format = js_date_format.replace(r'%d', 'dd')
    if '%' in js_date_format:
        js_date_format = ''
    if not js_date_format:
        js_date_format = 'yyyy-mm-dd'
    return js_date_format


def add_to_css_class(classes, new_class):
    new_class = new_class.strip()
    if new_class:
        # Turn string into list of classes
        classes = classes.split(" ")
        # Strip whitespace
        classes = [c.strip() for c in classes]
        # Remove empty elements
        classes = filter(None, classes)
        # Test for existing
        if not new_class in classes:
            classes.append(new_class)
            # Convert to string
        classes = u' '.join(classes)
    return classes


def create_prepend_append(**kwargs):
    tud = {}
    tud['append'] = kwargs.pop('append', None)
    tud['prepend'] = kwargs.pop('prepend', None)
    return tud, kwargs


def get_language():
    lang = translation.get_language()
    if '-' in lang:
        lang = '%s-%s' % (lang.split('-')[0].lower(), lang.split('-')[1].upper())
    return lang


def get_locale_js_url(lang):
    url = 'datepicker/js/locales/tud-datepicker.%s.js' % lang
    if finders.find(url):
        return settings.STATIC_URL + url
    if '-' in lang:
        return get_locale_js_url(lang.split('-')[0].lower())
    return ''


class StylingUneditableInput(forms.TextInput):

    def render(self, name, value, attrs=None):
        if attrs is None:
            attrs = {}
        attrs['type'] = 'hidden'
        klass = add_to_css_class(self.attrs.pop('class', ''), 'uneditable-input')
        klass = add_to_css_class(klass, attrs.pop('class', ''))
        base = super(StylingUneditableInput, self).render(name, value, attrs)
        return mark_safe(base + u'<span class="%s">%s</span>' % (klass, conditional_escape(value)))


class StylingTextInput(forms.TextInput):

    def __init__(self, *args, **kwargs):
        self.tud, kwargs = create_prepend_append(**kwargs)
        super(StylingTextInput, self).__init__(*args, **kwargs)


class StylingPasswordInput(forms.PasswordInput):

    def __init__(self, *args, **kwargs):
        self.tud, kwargs = create_prepend_append(**kwargs)
        super(StylingPasswordInput, self).__init__(*args, **kwargs)


class StylingDateInput(forms.DateInput):

    tud = {
        'append': mark_safe('<i class="icon-calendar"></i>'),
        'prepend': None,
    }

    @property
    def media(self):
        js = (
            settings.STATIC_URL + 'datepicker/js/tud-datepicker.js',
        )
        lang = get_language()
        if lang != 'en':
            locale_js_url = get_locale_js_url(lang)
            if locale_js_url:
                js = js + (
                    locale_js_url,
                )
        js = js + (
            settings.STATIC_URL + 'tud_styling/js/init_datepicker.js',
        )
        css = {
            'screen': (
                settings.STATIC_URL + 'datepicker/css/datepicker.css',
            )
        }
        return forms.Media(css=css, js=js)

    def render(self, name, value, attrs=None):
        date_input_attrs = {}
        if attrs:
            date_input_attrs.update(attrs)
        date_format = self.format
        if not date_format:
            date_format = default_date_format
        date_input_attrs.update({
            'data-date-format': javascript_date_format(date_format),
            'data-date-language': get_language(),
            'data-tud-widget': 'datepicker',
        })
        return super(StylingDateInput, self).render(name, value, attrs=date_input_attrs)
