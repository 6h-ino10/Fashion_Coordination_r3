from django.contrib import admin
from .models import Item,Coordination 
from django.utils.safestring import mark_safe


class ItemAdmin(admin.ModelAdmin):
    list_display=('id','name','season','category','image')

    def images(self,obj):
        return mark_safe('<img src="{}" style="width:100px height:auto;">'.format(obj.img.url))

admin.site.register(Item,ItemAdmin)


class CoordinationAdmin(admin.ModelAdmin):
    filter_horizontal = ('items',)

admin.site.register(Coordination,CoordinationAdmin)

