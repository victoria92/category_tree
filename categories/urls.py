from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from categories import views

urlpatterns = [
    path('categories/', views.category_list),
    path('categories/<int:pk>/', views.category_detail),
]

urlpatterns = format_suffix_patterns(urlpatterns)
