from django import template

register = template.Library()


@register.simple_tag
def is_task_done(task_done: bool, yes: str, no: str):
    return yes if task_done else no
