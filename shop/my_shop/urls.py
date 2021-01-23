from django.urls import path
from my_shop.views import *


urlpatterns = [
    path('', main_page, name='main_page'),
    path('create/', create_page, name='create_page'),
    path('<int:pid>/', details_page, name='post_detail'),
    path('<int:pid>/update/', update_page, name='post_update'),
]