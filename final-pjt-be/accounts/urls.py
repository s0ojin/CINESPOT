from django.urls import path
from . import views

appname = 'accounts'
urlpatterns = [
   path('user_info/<int:user_id>/', views.user_info), # 유저 정보여
]