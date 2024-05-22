from rest_framework import serializers
from .models import Movie, Review, Comment
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from .utils import get_user_profile_image

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


# 단일 영화 디테일 정보 조회
class MovieDetailSerializer(serializers.ModelSerializer):
    # 리뷰 목록만 조회해 볼게여 일단 ㅋㅋ
    # review_set = ReviewListSerializer(read_only=True, many=True) #원본
    # 05.22, 00:10, 영화 상세에는 달린 리뷰 6개만 보이기
    review_set = serializers.SerializerMethodField() #원본

    class Meta:
        model = Movie
        # Movie Detail 페이지에 영화 title과 review 목록만 노출하겠단 의미
        fields = ['id', 'title', 'overview','poster_path', 'backdrop_path', 'release_date', 'production_countries', 'runtime', 'genres', 'still_cut_paths', 'review_set']
        # fields = '__all__' 
    # 05.22, 00:10,
    # get_review_set(self, obj) 오버라이드해서 첫 6개 리뷰만 반환
    def get_review_set(self, obj):
        reviews = obj.review_set.all()[:6]
        return ReviewListSerializer(reviews, many=True).data


class ReviewListSerializer(serializers.ModelSerializer):
    # user = UserSerializer(read_only=True)  # 사용자 이름을 직렬화하기 위해 UserSerializer 사용
    user = serializers.SerializerMethodField()
    # 05.20,16:25, review_set 좋아요 기능 추가
    # like_count = serializers.SerializerMethodField()
    # 05.21,21:36, 리뷰에 달린 댓글 수 + 사용자 프로필 사진 기능 추가용
    comment_count = serializers.SerializerMethodField()
    userprofile = serializers.SerializerMethodField()
    
    class Meta:
        model = Review
        fields = ['id', 'user', 'userprofile', 'content', 'rating','comment_count'] # 추가할거 작성자 프로필 사진 경로, 댓글 수
        # fields = ['id', 'title', 'content', 'created_at', 'updated_at', 'movie', 'user', 'like_count', 'rating']

    def get_user(self, obj):
        return obj.user.username
    
    # 0520 1548 추가
    # def get_like_count(self, obj):
    #     return obj.likes.count()
    
    # 05.21,21:36, 이하상동
    def get_comment_count(self, obj):
        return obj.comments.count()
    def get_userprofile(self, obj):
        return get_user_profile_image(obj.user)


# 05.22,01:28
class CommentDetailSerializer(serializers.ModelSerializer):
    authorInfo = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['id', 'user', 'content', 'created_at', 'authorInfo']
        read_only_fields = ['user', 'created_at']

    def get_authorInfo(self, obj):
        return {
            "id": obj.user.id,
            "author": obj.user.username,
            "authorProfile": get_user_profile_image(obj.user)
        }

    def create(self, validated_data):
        request = self.context.get('request')
        review = validated_data.pop('review')
        user = request.user
        comment = Comment.objects.create(review=review, user=user, **validated_data)
        return comment



class ReviewDetailSerializer(serializers.ModelSerializer):
    authorInfo = serializers.SerializerMethodField()
    # 원본 movieInfo 필드
    # movieInfo = MovieDetailSerializer(source='movie', read_only=True)
    movieInfo = serializers.SerializerMethodField()
    # 원본 comments 필드
    # comments = CommentDetailSerializer(many=True, read_only=True, source='comment_set')
    comments = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()

    class Meta:
        model = Review
        fields = ['id', 'content', 'rating', 'likes_count', 'created_at', 'updated_at', 'authorInfo', 'movieInfo', 'comments']

    def get_authorInfo(self, obj):
        return {
            "id": obj.user.id,
            "author": obj.user.username,
            "authorProfile": get_user_profile_image(obj.user)
        }

    def get_likes_count(self, obj):
        return obj.likes.count()
    
    def get_comments(self, obj):
        comments = obj.comments.all()
        return CommentDetailSerializer(comments, many=True).data
    
    def get_movieInfo(self, obj):
        movie = obj.movie
        return {
            "id": movie.id,
            "title": movie.title,
            "poster_path": movie.poster_path,
            "production_countries": movie.production_countries,
            "release_date": movie.release_date,
            "genres": movie.genres,
            "runtime": movie.runtime,
        }



# 리뷰 생성하는 애
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



class CommentSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    userprofile = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['id', 'content', 'created_at', 'updated_at', 'user', 'userprofile']

    def get_user(self, obj):
        return obj.user.username

    def get_userprofile(self, obj):
        return get_user_profile_image(obj.user)