from django.contrib.postgres import fields
from django.urls import reverse
from django.utils.safestring import mark_safe
from django_json_widget.widgets import JSONEditorWidget
from django.contrib import admin
from .models import *


class ProductImagesInline(admin.StackedInline):
    model = Image


class ProductOptionsInline(admin.StackedInline):
    model = ProductOptions


class OptionGroupInline(admin.StackedInline):
    model = OptionGroup


class ProductInOrderInline(admin.StackedInline):
    model = ProductInOrder


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'options_display']
    list_filter = ['category']
    formfield_overrides = {
        fields.JSONField: {'widget': JSONEditorWidget},
    }
    inlines = [OptionGroupInline]
    prepopulated_fields = {'slug': ('name',)}

    def options_display(self, obj):
        key_value_pair = []
        for group in obj.option_groups.all():
            for opt in group.options.all():
                key_value_pair.append("<a href={}>{}</a>".
                format(
                reverse(
                    'admin:{}_{}_change'.format(opt._meta.app_label, opt._meta.model_name), args=(opt.pk,)),
                "{}={}".format(group.name, opt.option_value)))
        display_text = ", ".join(key_value_pair)
        if display_text:
            return mark_safe(display_text)
        return "-"


@admin.register(ProductOptions)
class ProductOptionsAdmin(admin.ModelAdmin):
    list_display = ['id', 'option_group', 'option_value', 'is_default']
    list_filter = ['option_group']
    formfield_overrides = {
        fields.JSONField: {'widget': JSONEditorWidget},
    }
    inlines = [ProductImagesInline]


@admin.register(OptionGroup)
class OptionGroupAdmin(admin.ModelAdmin):
    list_display = ['name', 'product']
    inlines = [ProductOptionsInline]


@admin.register(Order)
class OrderInAdmin(admin.ModelAdmin):
    list_display = ['client', 'create_date', 'total_price', 'status']
    list_filter = ['status']
    inlines = [ProductInOrderInline]


admin.site.register(Image)
admin.site.register(Client)
admin.site.register(Categories)
admin.site.register(ProductInOrder)
