from django import template
from better_profanity import profanity


register = template.Library()


@register.filter(name='censor')
def censor(value):
    censored = profanity.censor(value, '$')
    return censored