from django.contrib import admin
from .models import Client, Product, Order, ProductInOrder, Image


class ProductImagesInline(admin.StackedInline):
    model = Image


class ProductInOrderInline(admin.StackedInline):
    model = ProductInOrder


class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'category', 'description', 'attributes']
    list_filter = ['category']
    inlines = [ProductImagesInline]
    prepopulated_fields = {'slug': ('name',)}


class OrderInAdmin(admin.ModelAdmin):
    list_display = ['client', 'create_date', 'total_price', 'status']
    list_filter = ['status']
    inlines = [ProductInOrderInline]


admin.site.register(Client)
admin.site.register(Product, ProductAdmin)
admin.site.register(Image)
admin.site.register(Order, OrderInAdmin)
admin.site.register(ProductInOrder)
