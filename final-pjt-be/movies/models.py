from django.db import models
from django.conf import settings

# Create your models here.
# 영화 배우, 감독, 게시글 모델 구현

class Movie(models.Model):
    title = models.CharField(max_length = 150)
    actors = models.CharField(max_length = 150)
    director = models.CharField(max_length = 150)
    overview = models.TextField()
    relese_data = models.DateTimeField()
    poster_path = models.TextField() 

class Actor(models.Model):
    name =  models.CharField(max_length = 150)
'''
class Director(models.Model):
    pass
'''
class Comment(models.Model):
    content = models.TextField()
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)

class Movie_like_users(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)

