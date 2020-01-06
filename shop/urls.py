from django.template.context_processors import static
from django.urls import path, re_path
from django.conf import settings
from .views import basket, general_page, order, product_info

urlpatterns = [
    path('', general_page.index, name='general_page'),
    re_path('^basket/$', basket.index, name='basket_page'),
    re_path(r'^product/(?P<slug>[\w-]*)/$', product_info.ProductInfo.as_view()),
    # re_path(r'^product/(?P<slug>[\w-]*)/add_to_bag/$', product_info.ProductInfo.as_view())
]
