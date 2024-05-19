from django.db import models
from django.conf import settings

class Movie(models.Model):
    title = models.CharField(max_length=200)
    overview = models.TextField()
    release_date = models.DateField()
    vote_average = models.FloatField(null=True)
    vote_count = models.IntegerField(null=True)
    popularity = models.FloatField(null=True)
    poster_path = models.CharField(max_length=200, null=True)
    backdrop_path = models.CharField(max_length=200, null=True)
    original_language = models.CharField(max_length=10, null=True)
    genre_ids = models.JSONField(null=True)  # Django 3.1 이상에서 사용 가능
    raw_data = models.JSONField(null=True)  # 모든 데이터를 저장
    still_cut_paths = models.JSONField(null=True)  # 스틸컷 URL 저장

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
