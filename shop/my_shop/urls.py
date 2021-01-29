from django.urls import path
from my_shop.views import *


urlpatterns = [
    path('', main_page, name='main_page'),
    path('create/', create_page, name='create_page'),
    path('basket/', basket_page, name='basket_page'),
    path('search/', search_page, name='search_page'),
    path('<int:pid>/', details_page, name='post_detail'),
    path('<int:pid>/update/', update_page, name='post_update'),
]