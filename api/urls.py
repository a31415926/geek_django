from django.urls import path
from api import views
from rest_framework.urlpatterns import format_suffix_patterns


urlpatterns = [
    path('categories/', views.CategoriesView.as_view()),
    path('categories/<int:pk>', views.CategoriesDetailView.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
