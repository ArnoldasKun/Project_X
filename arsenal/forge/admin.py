from django.contrib import admin
from . import models


class OrderLineInline(admin.TabularInline):
    model = models.OrderLine
    extra = 0
    can_delete = False


class OrderLineAdmin(admin.ModelAdmin):
    list_display = ('unique_id', 'quantity', 'price', 'order', 'armor')
    ordering = ('order', 'unique_id')
    list_filter = ('order', 'armor')
    readonly_fields = ('unique_id', )
    #list_editable = ('status')
    fieldsets = (
        ('General', {'fields': ('unique_id', 'armor')}),
    )


class ArmorOrderAdmin(admin.ModelAdmin):
    search_fields = ('unique_id', 'armor__title', 'armor__blacksmith__last_name__exact', 'buyer__last_name')


class ArmorAdmin(admin.ModelAdmin):
    list_display = ('title', 'blacksmith')
    inlines = (OrderLineInline, )


class BlacksmithAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'display_armors')
    list_display_link = ('last_name', )


class ArmorReviewAdmin(admin.ModelAdmin):
    list_display = ('armor', 'buyer', 'created_at')

admin.site.register(models.ArmorType)
admin.site.register(models.Blacksmith, BlacksmithAdmin)
admin.site.register(models.Armor, ArmorAdmin)
admin.site.register(models.Buyer)
admin.site.register(models.ArmorOrder, ArmorOrderAdmin)
admin.site.register(models.OrderLine, OrderLineAdmin)
admin.site.register(models.ArmorReview, ArmorReviewAdmin)
