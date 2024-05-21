from django.urls import path
from . import views

appname = 'movies'
urlpatterns = [
   path('movies/', views.movie_list), # 영화 리스트 조회
   path('movies/<int:movie_pk>/', views.movie_detail), # 영화 상세 내용 조회
   path('movies/<int:movie_pk>/reviews/', views.create_review), # 리뷰 생성
   path('movies/<int:movie_pk>/review_list/', views.review_list), # 영화에 달린 모든 리뷰 리스트 조회
   path('reviews/<int:review_pk>/', views.review_detail),
   # 영화 좋아요 기능 확인 임시 경로
   path('movies/<int:movie_pk>/like/', views.movie_like_users),
   # 리뷰 좋아요 기능 확인 임시 경로
   path('reviews/<int:review_pk>/like/', views.review_like_users),
]

