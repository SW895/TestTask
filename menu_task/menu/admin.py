from django.contrib import admin

# Register your models here.
from .models import Menu, MenuItem

#admin.site.register(Menu)
#admin.site.register(MenuItem)


class MenuItemInline(admin.TabularInline):
    model = MenuItem
    fields = ('name', 'parent')
    

class MenuAdmin(admin.ModelAdmin):
    inlines = [MenuItemInline,]


admin.site.register(Menu, MenuAdmin)