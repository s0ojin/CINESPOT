from django.db import models

class Movie(models.Model):
    title = models.CharField(max_length=200)
    overview = models.TextField()
    release_date = models.DateField()
    vote_average = models.FloatField(null=True)
    vote_count = models.IntegerField(null=True)
    popularity = models.FloatField(null=True)
    poster_path = models.CharField(max_length=200, null=True)
    # backdrop_path = models.CharField(max_length=200, null=True)
    # original_language = models.CharField(max_length=10, null=True)
    genre_ids = models.JSONField(null=True)  # Django 3.1 이상에서 사용 가능
    # raw_data = models.JSONField(null=True)  # 모든 데이터를 저장

    def __str__(self):
        return self.title
