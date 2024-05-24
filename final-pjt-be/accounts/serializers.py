from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from .utils import get_user_profile_image
from movies.models import Movie, Review, Movie_likes_users, Review_likes_users
from movies.serializers import MovieSerializer, ReviewListSerializer

User = get_user_model()

class UserInfoSerializer(serializers.ModelSerializer):
    userprofile = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ['id','username','userprofile']
    
    # def get_user(self, obj):
    #     return obj.user.username
    
    def get_userprofile(self, obj):
        if hasattr(obj, 'profile') and obj.profile.image:
            return obj.profile.image.url
        return None


class UserProfileSerializer(serializers.ModelSerializer):
    userprofile = serializers.SerializerMethodField()
    liked_movies = serializers.SerializerMethodField()
    reviewed_movies = serializers.SerializerMethodField()
    review_liked_movies = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'userprofile', 'liked_movies', 'reviewed_movies', 'review_liked_movies']

    def get_userprofile(self, obj):
        if hasattr(obj, 'profile') and obj.profile.image:
            return obj.profile.image.url
        return None

    def get_liked_movies(self, obj):
        liked_movies = obj.liked_movies.all()
        context = self.context  # context를 가져와서 전달
        return MovieSerializer(liked_movies, many=True, context=context).data

    def get_reviewed_movies(self, obj):
        reviews = Review.objects.filter(user=obj)
        context = self.context  # context를 가져와서 전달
        return ReviewListSerializer(reviews, many=True, context=context).data

    def get_review_liked_movies(self, obj):
        review_likes = Review_likes_users.objects.filter(user=obj)
        reviews = [review_like.review for review_like in review_likes]
        context = self.context  # context를 가져와서 전달
        return ReviewListSerializer(reviews, many=True, context=context).data
    
    # 원본
    # def get_liked_movies(self, obj):
    #     liked_movies = Movie.objects.filter(liked_movies=obj)
    #     return MovieSerializer(liked_movies, many=True).data

    # def get_reviewed_movies(self, obj):
    #     reviews = Review.objects.filter(user=obj)
    #     return ReviewListSerializer(reviews, many=True).data

    # def get_review_liked_movies(self, obj):
    #     review_likes = Review_likes_users.objects.filter(user=obj)
    #     reviews = [review_like.review for review_like in review_likes]
    #     return ReviewListSerializer(reviews, many=True).data