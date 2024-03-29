from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from categories import views

urlpatterns = [
    path("categories/", views.CategoryList.as_view()),
    path("categories/<int:pk>/", views.CategoryDetail.as_view()),
    path("categories/<int:pk>/upload/", views.ImageUploadView.as_view()),
    path("categories/<int:pk>/similar/", views.SimilarityDetail.as_view()),
    path("categories/<int:pk>/<type>/", views.CategoryTreeListing.as_view()),
    path("similarity/", views.SimilarityList.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
