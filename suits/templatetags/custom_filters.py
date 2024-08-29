from django import template
from django.utils.html import format_html, strip_tags
import datetime

register = template.Library()

# --- Filters ---

@register.filter(name='length_is')
def length_is(value, arg):
    """Check if the length of the value equals the given number."""
    try:
        return len(value) == int(arg)
    except (TypeError, ValueError):
        return False

@register.filter(name='truncate')
def truncate(value, length):
    """Truncate a string to the specified length."""
    try:
        length = int(length)
        return value[:length] if isinstance(value, str) else value
    except (ValueError, TypeError):
        return value

@register.filter(name='uppercase')
def uppercase(value):
    """Convert a string to uppercase."""
    return value.upper() if isinstance(value, str) else value

@register.filter(name='lowercase')
def lowercase(value):
    """Convert a string to lowercase."""
    return value.lower() if isinstance(value, str) else value

@register.filter(name='capitalize')
def capitalize(value):
    """Capitalize the first letter of a string."""
    return value.capitalize() if isinstance(value, str) else value

@register.filter(name='reverse')
def reverse(value):
    """Reverse a string."""
    return value[::-1] if isinstance(value, str) else value

@register.filter(name='date_format')
def date_format(value, format_string):
    """Format a date according to the given format string."""
    if isinstance(value, datetime.date):
        return value.strftime(format_string)
    return value

@register.filter(name='replace')
def replace(value, old, new):
    """Replace occurrences of old with new in the string."""
    return value.replace(old, new) if isinstance(value, str) else value

@register.filter(name='strip_html')
def strip_html(value):
    """Remove HTML tags from a string."""
    return strip_tags(value) if isinstance(value, str) else value

@register.filter(name='currency')
def currency(value, symbol='$'):
    """Format a number as currency."""
    try:
        return format_html(f"{symbol}{float(value):,.2f}")
    except (ValueError, TypeError):
        return value

@register.filter(name='join_with')
def join_with(value, separator):
    """Join items in a list or tuple with the given separator."""
    if isinstance(value, (list, tuple)):
        return separator.join(map(str, value))
    return value

@register.filter(name='get_item')
def get_item(value, index):
    """Get an item from a list or dictionary by index or key."""
    try:
        return value[index]
    except (IndexError, KeyError, TypeError):
        return None

# --- Template Tags ---

@register.simple_tag
def greet(name):
    """Return a greeting message."""
    return f"Hello, {name}!"

@register.simple_tag
def current_year():
    """Return the current year."""
    return datetime.datetime.now().year

@register.simple_tag
def full_name(first_name, last_name):
    """Return the full name by combining first and last names."""
    return f"{first_name} {last_name}"

@register.simple_tag
def is_odd(number):
    """Check if a number is odd."""
    try:
        return int(number) % 2 != 0
    except (ValueError, TypeError):
        return False

@register.simple_tag
def format_date(date, format_string='%Y-%m-%d'):
    """Format a date object or string."""
    if isinstance(date, datetime.date):
        return date.strftime(format_string)
    try:
        date_obj = datetime.datetime.strptime(date, '%Y-%m-%d')
        return date_obj.strftime(format_string)
    except (ValueError, TypeError):
        return date

@register.simple_tag
def toggle(value, on_value, off_value):
    """Toggle between two values."""
    return on_value if value else off_value
@register.filter(name='add_class')
def add_class(field, css_class):
    """Add a CSS class to a form field's HTML."""
    if hasattr(field, 'as_widget'):
        return format_html(
            '<{tag} class="{class_attr}"{attrs}>{label}{errors}{help_text}{widget}</{tag}>',
            tag='div',
            class_attr=css_class,
            attrs='',
            label=field.label_tag() if field.label else '',
            errors=field.errors.as_ul() if field.errors else '',
            help_text=field.help_text or '',
            widget=field.as_widget(attrs={'class': css_class}),
        )
    return field