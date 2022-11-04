from django import template

register = template.Library()


@register.filter(name="calc_total")
def calc_total(arg):
    return sum(d.get('amount') for d in arg)