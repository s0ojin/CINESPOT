from django.urls import path
from . import views

appname = 'movies'
urlpatterns = [
   path('movies/', views.movie_list),
   path('movies/<int:movie_pk>/', views.movie_detail),
   path('reviews/', views.review_list),
   path('reviews/<int:review_pk>/', views.review_detail),
   path('movies/<int:movie_pk>/reviews/', views.create_review),
   # review_list test url
   # path('movies/<int:movie_pk>/review-list/', views.movie_review_list),
]

