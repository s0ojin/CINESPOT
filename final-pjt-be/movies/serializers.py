from rest_framework import serializers
from .models import Movie, Review
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username']


class MovieContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ('title',)

class MovieSerialzer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ('title', 'overview')

class ReviewListSerializer(serializers.ModelSerializer):
    # 원래 코드
    # class Meta:
    #     model = Review
    #     fields = '__all__'
    # user = UserSerializer(read_only=True)  # 사용자 이름을 직렬화하기 위해 UserSerializer 사용

    class Meta:
        model = Review
        fields = ['id', 'title', 'content', 'created_at', 'updated_at', 'movie', 'user']

# 단일 영화 정보 제공
class MovieDetailSerializer(serializers.ModelSerializer):
    # class ActorNameSerializer(serializers.ModelSerializer):
        # class Meta:
        #     model = Actor
        #     fields = ('name',)
    # 리뷰 목록만 조회해 볼게여 일단 ㅋㅋ
    # actors = ActorNameSerializer(Movie.actors, many=True, read_only=True)
    
    review_set = ReviewListSerializer(Movie.review_set, read_only=True, many=True)

    class Meta:
        model = Movie
        fields = ('title','review_set',) 
        # Movie Detail 페이지에 영화 title과 review 목록만 노출하겠단 의미


class ReviewDetailSerializer(serializers.ModelSerializer):
    movie = MovieContentSerializer(Review.movie, read_only=True)
    class Meta:
        model = Review
        fields = '__all__'

class ReviewGenSerializer(serializers.ModelSerializer):
    # user: <int> -> user: <username>으로 보기위해 아래 코드 추가
    # user = UserSerializer(read_only=True) 
    # movie = MovieContentSerializer(read_only=True)
    movie = MovieContentSerializer(Review.movie, read_only=True) # 원본
    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ('user','movie')

    def create(self, validated_data):
        user = self.context['request'].user
        movie = self.context['movie']
        validated_data['user'] = user
        validated_data['movie'] = movie
        return super().create(validated_data)



