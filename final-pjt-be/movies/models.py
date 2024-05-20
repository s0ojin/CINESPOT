from django.db import models
from django.conf import settings

class Movie(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=255)
    overview = models.TextField()
    release_date = models.DateField()
    poster_path = models.CharField(max_length=255, null=True)
    genre_ids = models.JSONField(null=True)  # Django 3.1 이상에서 사용 가능
    production_countries = models.JSONField(null=True)
    still_cut_paths = models.JSONField(null=True)  # 스틸컷 URL 저장
    runtime = models.IntegerField(null=True)  # 런닝 타임 저장(단위:분)
    liked_movies = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='liked_movies', blank=True)
    # vote_average = models.FloatField(null=True)
    # vote_count = models.IntegerField(null=True)
    # popularity = models.FloatField(null=True)
    # backdrop_path = models.CharField(max_length=200, null=True)
    # original_language = models.CharField(max_length=10, null=True)
    # raw_data = models.JSONField(null=True)  # 모든 데이터를 저장


    def __str__(self):
        return self.title


class Review(models.Model): ## 우리의 게시글 커뮤니티
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='review_set') # 게시글에 해당하는 영화 정보
    user = models.ForeignKey(settings.AUTH_USER_MODEL , on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True) # 생성일
    updated_at = models.DateTimeField(auto_now=True)    # 수정일
    # 좋아요 필드는 어카지
    
    def __str__(self):
        return self.title

class Movie_likes_users(models.Model):
    # movie = models.ForeignKey(Movie, on_delete=models.CASCADE) # 원본
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='liked_movie')

class Review_likes_users(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='liked_review')
    