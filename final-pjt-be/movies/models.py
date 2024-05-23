from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model


class Movie(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=255)
    overview = models.TextField()
    release_date = models.DateField()
    poster_path = models.CharField(max_length=255, null=True)
    genres = models.JSONField(null=True)  # 장르 'name'형태 저장
    genre_ids = models.JSONField(null=True)  # Django 3.1 이상에서 사용 가능
    production_countries = models.JSONField(null=True)
    still_cut_paths = models.JSONField(null=True)  # 스틸컷 URL 저장
    runtime = models.IntegerField(null=True)  # 런닝 타임 저장(단위:분)
    backdrop_path = models.CharField(max_length=200, null=True)
    liked_movies = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='liked_movies', blank=True)
    similarity_score = models.FloatField(default=0.0)  # 추천을 위한 유사도 저장 필드
    popularity = models.FloatField(null=True, blank=True)  # 인기도 점수 추가
    vote_average = models.FloatField(null=True, blank=True)  # 평점 점수 추가
    
    def __str__(self):
        return self.title


class Review(models.Model): ## 우리의 게시글 커뮤니티
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='review_set') # 게시글에 해당하는 영화 정보
    user = models.ForeignKey(settings.AUTH_USER_MODEL , on_delete=models.CASCADE)
    # title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True) # 생성일
    updated_at = models.DateTimeField(auto_now=True)    # 수정일
    # rating = models.PositiveIntegerField()  # 별점 필드 추가 정수 단위 별점
    rating = models.DecimalField(max_digits=3, decimal_places=1)  # 0.5 단위로 별점
    # likestatus = models.ManyToManyField(get_user_model(), related_name='liked_reviews', blank=True)

    def __str__(self):
        return self.content
    # def __str__(self):
    #     return self.title


class Movie_likes_users(models.Model):
    # movie = models.ForeignKey(Movie, on_delete=models.CASCADE) # 원본
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='liked_movie')


class Review_likes_users(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='liked_review')



class Comment(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)   
    
    def __str__(self):
        return self.content