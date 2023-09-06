from django import template

register = template.Library()

@register.filter
def previous(queryset, current_index):
    try:
        return queryset[int(current_index) - 1] 
    except:
        return '' 

@register.filter
def get_value(data, key):
    return data.get(key)