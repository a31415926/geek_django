from django.urls import path
from my_shop.views import *


urlpatterns = [
    path('', main_page, name='main_page'),
    path('basket/', basket_page, name='basket_page'),
    path('checkout/', checkout_page, name='checkout_page'),
    path('create/', create_page, name='create_page'),
    path('create_cats/', create_cats, name='create_cats'),
    path('search/', search_page, name='search_page'),
    path('<int:pid>/', details_page, name='post_detail'),
    path('<int:pid>/update/', update_page, name='post_update'),
    path('cats/<int:pid>/', cats_page, name='cats_page'),
]