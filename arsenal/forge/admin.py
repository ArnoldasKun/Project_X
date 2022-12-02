from django.contrib import admin
from . import models


class OrderLineInline(admin.TabularInline):
    model = models.OrderLine
    extra = 0
    can_delete = False


class ArmorAdmin(admin.ModelAdmin):
    list_display = ('title', 'blacksmith')
    inlines = (OrderLineInline, )


class BlacksmithAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'display_armors')
    list_display_link = ('last_name', )

admin.site.register(models.ArmorType)
admin.site.register(models.Blacksmith, BlacksmithAdmin)
admin.site.register(models.Armor, ArmorAdmin)
admin.site.register(models.Buyer)
admin.site.register(models.ArmorOrder)
admin.site.register(models.OrderLine)
