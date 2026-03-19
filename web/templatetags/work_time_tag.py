from django import template
register = template.Library()

@register.simple_tag
def work_time():
    return f"⏰ Monday - Saturday: 09:00 - 20:00"