from django.db import models
from django.urls import reverse
# Create your models here.

class Menu(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name
    
class MenuItem(models.Model):
    name = models.CharField(max_length=200)
    rank = models.IntegerField(blank=True, null=True)
    parent = models.ForeignKey('self', verbose_name='parent', on_delete=models.CASCADE, blank=True, null=True)
    menu = models.ForeignKey('Menu', on_delete=models.CASCADE)
    view_order = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('index', kwargs={'active_menu':self.menu.pk, 'active_item':self.pk})

    def save(self, *args, **kwargs):
        global view_order, obj
        view_order = 0
        obj = []

        if self.parent:
            self.rank = self.parent.rank + 1
        else:
            self.rank = 0
            
        super(MenuItem, self).save(*args, **kwargs)
        
        items = MenuItem.objects.filter(menu=self.menu).order_by('name')       
        set_view_order(items)
        MenuItem.objects.bulk_update(obj,['view_order'])
    

def set_view_order(queryset, parent_id=None):
    global view_order, obj
    for item in queryset.filter(parent=parent_id):        
        view_order += 1
        item.view_order = view_order
        obj.append(item)        
        set_view_order(queryset, item.pk)
