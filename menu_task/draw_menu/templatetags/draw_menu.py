from menu.models import MenuItem, Menu
from django import template

register = template.Library()

@register.inclusion_tag('menu.html', takes_context=True)
def draw_menu(context, menu_items):
    active_item = context['active_item']
    rank_diff = {}
    previous = None
    for item in menu_items:
        if previous == None:
            previous = item
            continue            
        if previous.rank - item.rank > 1:
            rank_diff[item.name] = range(1, previous.rank-item.rank + 1)
        previous = item
    return {
        'local_menu': menu_items,
        'rank_diff':rank_diff,
        'active_item':active_item,
        }

