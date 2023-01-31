from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()


@register.filter
@stringfilter
def time_beautifier(value):
    if value == "":
        return ""
    v = value
    hour_string = ""
    minute_string = ""
    dot_count = 0
    for c in value:
        if c == '.':
            dot_count += 1
            if dot_count == 2:
                break
        else:
            if dot_count == 0:
                hour_string += c
            if dot_count == 1:
                minute_string += c
    hour = int(hour_string)
    if hour > 12:
        return str(hour - 12) + ":" + minute_string + "PM"
    if hour == 12:
        return str(hour) + ":" + minute_string + "PM"
    if hour == 0:
        return "12:" + minute_string + "AM"
    else:
        return str(hour) + ":" + minute_string + "AM"
