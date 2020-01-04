from django.urls import path
from .views import basket, general_page, order, product_info

urlpatterns = [
    path('', general_page.index, name='general_page'),
    path('basket/', basket.index, name='basket_page'),
    path('order/', order.order_index, name='order_page')
]