from django.urls import path
from . import views

appname = 'movies'
urlpatterns = [
   path('movies/', views.movie_list),
   path('movies/<int:movie_pk>/', views.movie_detail),
   path('reviews/', views.review_list),
   path('reviews/<int:review_pk>/', views.review_detail),
   path('movies/<int:movie_pk>/reviews/', views.create_review),
   # 영화 좋아요 기능 확인 임시 경로
   path('movies/<int:movie_pk>/like/', views.movie_like_users),
   # 리뷰 좋아요 기능 확인 임시 경로
   path('reviews/<int:review_pk>/like/', views.review_like_users),

]

