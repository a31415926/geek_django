from django.contrib import admin
from django.urls import path
from django.urls import include


urlpatterns = [
    path('', include('my_shop.urls')),
    path('', include('accounts.urls')),
    path('api/', include('api.urls')),
    path('olx/', include('olx.urls')),
    path('admin/', admin.site.urls),

]
