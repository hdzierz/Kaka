from django import template

register = template.Library()

@register.filter(name='pdb') 
def pdb(element):
    import pdb; pdb.set_trace()
    return element
