from django import template

register = template.Library()


@register.filter(name='loop')
def perform_loop(nums: int) -> range:
    return range(nums)


@register.filter(name='replace_word')
def replace(word: str):
    return word.replace(' ', '-')
