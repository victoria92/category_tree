from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from categories import views

urlpatterns = [
    path("categories/", views.CategoryList.as_view()),
    path("categories/<int:pk>/", views.CategoryDetail.as_view()),
    path("categories/<int:pk>/upload/", views.ImageUploadView.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
