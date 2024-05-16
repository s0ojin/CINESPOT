from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
# 회원 모델 구현
class User(AbstractUser):
    followings = models.ManyToManyField('self', symmetrical=False, related_name='followers')
    # pass # 팔로워 기능 구현 안할 때