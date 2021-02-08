from django.urls import path
from my_shop.views import *


urlpatterns = [
    path('', HomePage.as_view(), name='main_page'),
    path('basket/', basket_page, name='basket_page'),
    path('checkout/', CheckoutPage.as_view(), name='checkout_page'),
    path('create/', CreateGoodsView.as_view(), name='create_page'),
    path('create_cats/', CreateCategoryView.as_view(), name='create_cats'),
    path('search/', SearchPageView.as_view(), name='search_page'),
    path('<int:pk>/', details_page, name='post_detail'),
    path('<int:pk>/update/', UpdateGoodsView.as_view(), name='post_update'),
    path('cats/<int:pk>/', CategoryPage.as_view(), name='cats_page'),
]