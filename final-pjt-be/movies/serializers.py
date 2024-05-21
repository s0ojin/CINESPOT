from rest_framework import serializers
from .models import Movie, Review
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username']


class MovieContentSerializer(serializers.ModelSerializer): # 이거 좀 무쓸모 같은데,,
    class Meta:
        model = Movie
        fields = ('title',)

# 영화 리스트 조회 페이지
class MovieSerializer(serializers.ModelSerializer):
    # 05.20/23:35 추가
    is_liked = serializers.SerializerMethodField()
    class Meta:
        model = Movie
        fields = ('id','title','release_date', 'production_countries', 'poster_path', 'is_liked')
        # fields = '__all__'
    
    # 05.20/23:35 추가
    def get_is_liked(self, obj):
        request = self.context.get('request', None)
        if request and request.user.is_authenticated:
            return request.user in obj.liked_movies.all()
        return False



class ReviewListSerializer(serializers.ModelSerializer):
    # user = UserSerializer(read_only=True)  # 사용자 이름을 직렬화하기 위해 UserSerializer 사용
    user = serializers.SerializerMethodField()
    # 05.20,16:25, review_set 좋아요 기능 추가
    like_count = serializers.SerializerMethodField()
    class Meta:
        model = Review
        fields = ['id', 'content', 'created_at', 'updated_at', 'movie', 'user', 'like_count', 'rating']
        # fields = ['id', 'title', 'content', 'created_at', 'updated_at', 'movie', 'user', 'like_count', 'rating']

    def get_user(self, obj):
        return obj.user.username
    
    # 0520 1548 추가
    def get_like_count(self, obj):
        return obj.likes.count()
    


# 단일 영화 정보 제공
class MovieDetailSerializer(serializers.ModelSerializer):
    # 리뷰 목록만 조회해 볼게여 일단 ㅋㅋ
    review_set = ReviewListSerializer(read_only=True, many=True) #원본

    class Meta:
        model = Movie
        # Movie Detail 페이지에 영화 title과 review 목록만 노출하겠단 의미
        # fields = ('title','review_set') 
        fields = '__all__' 


class ReviewDetailSerializer(serializers.ModelSerializer):
    # user = UserSerializer(read_only=True) # "user" : {'username':'harry'} ver.
    # movie = MovieContentSerializer(Review.movie, read_only=True) #원본
    user = serializers.SerializerMethodField() # "user" : 'harry' ver.
    movie = MovieContentSerializer(read_only=True)
    # 0520 1548 추가
    like_count = serializers.SerializerMethodField()

    class Meta:
        model = Review
        fields = '__all__'
    
    def get_user(self, obj):
        return obj.user.username
    
    # 0520 1548 추가
    def get_like_count(self, obj):
        return obj.likes.count()
    

class ReviewGenSerializer(serializers.ModelSerializer):
    # user: <int> -> user: <username>으로 보기위해 아래 코드 추가
    # user = UserSerializer(read_only=True) # "user" : {'username':'harry'} ver.
    # movie = MovieContentSerializer(Review.movie, read_only=True) # 원본
    user = serializers.SerializerMethodField() # "user" : 'harry' ver.
    movie = MovieContentSerializer(read_only=True) # 변경
    class Meta:
        model = Review
        fields = ['id', 'content', 'created_at', 'updated_at', 'movie', 'user', 'rating']
        # fields = ['id', 'title', 'content', 'created_at', 'updated_at', 'movie', 'user', 'rating']
        read_only_fields = ('user','movie')

    def get_user(self, obj):
        return obj.user.username

    def create(self, validated_data):
        user = self.context['request'].user
        movie = self.context['movie']
        validated_data['user'] = user
        validated_data['movie'] = movie
        return super().create(validated_data)
