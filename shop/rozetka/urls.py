from django.urls import path
from rozetka.views import *


urlpatterns = [
    path('', main_page, name='rozetka_main_page'),
    path('cats/<int:cat_id>/', goods_of_cats, name='goods_list_cats_page'),
    path('parser/', parser_goods, name='parser_page'),
]