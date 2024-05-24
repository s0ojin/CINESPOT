# recommendations/urls.py
from django.urls import path
from .views import recommend_destinations

urlpatterns = [
    path('recommend/', recommend_destinations),
]
