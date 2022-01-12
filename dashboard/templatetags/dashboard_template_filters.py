from django import template

register = template.Library()


@register.filter(name='loop')
def perform_loop(nums: int) -> range:
    return range(nums)


def attribute_generator():
    return (attr for attr in ['Articles', 'PDFs', 'Online Classes', 'Videos', 'Questions'])


@register.simple_tag
def guide_attributes():
    generator = attribute_generator()
    try:
        return next(generator)
    except StopIteration:
        return
