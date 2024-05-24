from django.urls import path
from . import views

appname = 'accounts'
urlpatterns = [
   path('user_info/', views.user_info), # 유저 정보여
   path('my_page/', views.my_page), # 마이페이지용
]