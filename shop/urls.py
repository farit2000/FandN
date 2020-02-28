from django.template.context_processors import static
from django.urls import path, re_path
from django.conf import settings
from .views import basket, general_page, order, product_info, success, test

urlpatterns = [
    path('', general_page.index, name='general_page'),
    re_path(r'^product/(?P<slug>[\w-]*)/$', product_info.ProductInfo.as_view()),
    path('basket/', basket.index, name='basket_page'),
    path('order/', order.order_index, name='order_page'),
    path('success/', success.index, name='success'),
    path('test/', test.index, name='test'),
]
