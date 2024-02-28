from django import template

register = template.Library()

@register.filter
def first_n_sentences(value, n):
    sentences = value.split('. ')
    return '. '.join(sentences[:n]) + '.' if len(sentences) > n else value