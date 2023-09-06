from django.shortcuts import render
from .models import Menu, MenuItem

# Create your views here.

def index(request,active_menu=None, active_item=None):
    items_dict = {}
    menus = Menu.objects.all()

    for menu in menus:
        if menu.pk != active_menu:
            menu_items = MenuItem.objects.filter(menu=menu,parent=None).order_by('view_order')
            items_dict[menu.name] = menu_items
        else:
            menu_items = MenuItem.objects.raw("WITH CTE AS (\
                                        SELECT id, parent_id, name, view_order, menu_id \
                                            FROM menu_MenuItem \
                                            WHERE (parent_id is NULL AND menu_id=%s) OR parent_id=%s OR id=%s\
                                        UNION \
                                        SELECT t.id, t.parent_id, t.name, t.view_order, t.menu_id \
                                            FROM menu_MenuItem as t\
                                        INNER JOIN CTE c\
                                        ON  t.id = c.parent_id \
                                            OR \
                                            t.parent_id = c.parent_id)\
                                        SELECT * \
                                            FROM CTE \
                                            ORDER BY menu_id, view_order;", [str(active_menu), str(active_item), str(active_item)]) 
            items_dict[menu.name] = menu_items

    if request.GET:
        draw_pk = int(request.GET['menu'])  
        draw = MenuItem.objects.filter(menu=draw_pk).order_by('view_order')
    else:
        draw_pk = None 
        draw = None
        
    return render(
        request,
        'base.html',
        context = {
            'menus':menus,
            'items_dict':items_dict,
            'active_item':active_item,            
            'draw':draw,
            'draw_pk':draw_pk,
        }
    )



