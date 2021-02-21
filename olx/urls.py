from django.urls import path
from olx.views import *

urlpatterns = [
    path('parse/', parse_page),
]
