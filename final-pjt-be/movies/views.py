from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Movie, Review, Review_likes_users, Comment
from .serializers import MovieSerializer, MovieDetailSerializer, MovieRecommendationSerializer
from .serializers import ReviewListSerializer, ReviewDetailSerializer, ReviewGenSerializer
from .serializers import CommentSerializer
from django.contrib.auth import get_user_model

from .recommand import compute_cosine_similarity, personalized_score

@api_view(['GET'])
def movie_review_list(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    # reviews = movie.reviews.all()  # 역참조를 사용하여 리뷰를 가져옵니다
    reviews = movie.review_set.all()  # 역참조를 사용하여 리뷰를 가져옵니다
    serializer = ReviewListSerializer(reviews, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def movie_list(request):
    movies = Movie.objects.all()
    # 원본 코드
    # serializer = MovieSerializer(movies, many=True)
    serializer = MovieSerializer(movies, many=True, context={'request': request})
    return Response(serializer.data, status=status.HTTP_200_OK)

# 영화 상세 내역 조회 원본 코드
@api_view(['GET'])
def movie_detail(request,movie_pk):
    # 원본
    # movie= Movie.objects.get(pk=movie_pk)
    movie = get_object_or_404(Movie, pk=movie_pk)
    serializer = MovieDetailSerializer(movie, context={'request': request})
    # serializer = MovieDetailSerializer(movie)
    return Response(serializer.data, status=status.HTTP_200_OK)


# 리뷰 목록 조회 뷰함수
# 05.22, 00:32, 전체 수정
@api_view(['GET'])
def review_list(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    # 원본 코드
    # reviews = Review.objects.all()
    reviews = Review.objects.filter(movie=movie)
    # serializer = ReviewListSerializer(reviews, many=True)
    serializer = ReviewListSerializer(reviews, many=True, context={'request': request})
    return Response(serializer.data, status=status.HTTP_200_OK)


# 영화 별 리뷰 생성
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_review(request, movie_pk):
    # movie = Movie.objects.get(pk=movie_pk)
    movie = get_object_or_404(Movie, pk=movie_pk)
    serializer = ReviewGenSerializer(data=request.data,  context={'request': request, 'movie': movie})
    if serializer.is_valid(raise_exception=True):
        serializer.save()
        # serializer.save(movie=movie)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET', 'PUT', 'DELETE'])
def review_detail(request, review_pk):
    review = get_object_or_404(Review, pk=review_pk)
    if request.method == 'GET':
        # serializer = ReviewDetailSerializer(review)
        serializer = ReviewDetailSerializer(review, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    elif request.method == 'PUT':
        serializer = ReviewDetailSerializer(review, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
    elif request.method == 'DELETE':
        review.delete()
        return Response({'message': f'review {review_pk} is deleted.'}, status=status.HTTP_204_NO_CONTENT)


    
# 영화 좋아요
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def movie_like_users(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)

    if request.user in movie.liked_movies.all():
        movie.liked_movies.remove(request.user)
        liked = False
    else:
        movie.liked_movies.add(request.user)
        liked = True
        
    return Response({'liked':liked}, status=status.HTTP_200_OK)

# 리뷰 좋아요 뷰
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def review_like_users(request, review_pk):
    review = get_object_or_404(Review, pk=review_pk)
    user = request.user

 # 본인이 작성한 리뷰에는 좋아요를 누를 수 없음
    if review.user == user:
        return Response({'error': 'You cannot like your own review.'}, status=status.HTTP_403_FORBIDDEN)

    # Review_likes_users 모델을 사용하여 좋아요 추가/삭제
    review_like, created = Review_likes_users.objects.get_or_create(review=review, user=user)

    if not created:
        # 이미 좋아요를 누른 경우 좋아요를 취소
        review_like.delete()
        liked = False
    else:
        liked = True

    return Response({'liked': liked, 'like_count': review.likes.count()}, status=status.HTTP_200_OK)


# 05.22, 14:37분 갈아 엎는 중
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def comment_list_create(request, review_pk):
    review = get_object_or_404(Review, pk=review_pk)
    
    if request.method == 'GET':
        comments = Comment.objects.filter(review=review)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

       
# 특정 리뷰에 대한 댓글 생성 함수 ; 정상 동작 확인(05.22,15:49)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_comment(request, review_pk):
    review = get_object_or_404(Review, pk=review_pk)
    serializer = CommentSerializer(data=request.data, context={'request': request, 'review': review})
    if serializer.is_valid(raise_exception=True):
        serializer.save(user=request.user, review=review)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 특정 리뷰에 달린 댓글 수정/삭제 함수 ; DELETE 정상 동작 확인(05.22,15:49)
@api_view(['PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def comment_detail(request, comment_pk):
    if request.method == 'PUT':
        # 댓글 수정
        comment = get_object_or_404(Comment, pk=comment_pk)
        data = request.data
        content = data.get('content')

        if not content:
            return Response({'error': 'Content is required'}, status=status.HTTP_400_BAD_REQUEST)

        comment.content = content
        comment.save()
        response_data = {
            'id': comment.id,
            'content': comment.content,
            'created_at': comment.created_at,
            'updated_at': comment.updated_at,
            'user': comment.user.username,
            # 'userprofile': get_user_profile_image(comment.user)
        }
        return Response(response_data, status=status.HTTP_200_OK)

    elif request.method == 'DELETE':
        # 댓글 삭제
        comment = get_object_or_404(Comment, pk=comment_pk)
        comment.delete()
        return Response({'message': 'Comment deleted'}, status=status.HTTP_204_NO_CONTENT)
    


# View for movie recommamdation service
@api_view(['GET'])
def genre_recommendations(request):
   # 현재 로그인한 사용자의 정보 가져오기
    user = request.user

    if user.is_authenticated:
        # 사용자가 좋아하는 영화의 장르 정보 가져오기
        user_liked_genres = [genre for movie in user.liked_movies.all() for genre in movie.genres]

        # 모든 영화의 장르 정보 가져오기
        all_movies = Movie.objects.exclude(id__in=user.liked_movies.all().values_list('id', flat=True))
        
        # 유사도 계산
        similarities = []
        for movie in all_movies:
            similarity = compute_cosine_similarity(user_liked_genres, movie.genres)
            similarities.append((movie.title, similarity))

        # 유사도에 따라 정렬
        sorted_similarities = sorted(similarities, key=lambda x: x[1], reverse=True)
        # 상위 10개의 유사한 영화 추출
        top_similar_movies = sorted_similarities[:10]
        # print(top_similar_movies)

        # 추천 영화 정보 가져오기
        recommended_movie_titles = [movie[0] for movie in top_similar_movies]
        recommended_movies = []
        for title in recommended_movie_titles:
            movie = Movie.objects.get(title=title)
            recommended_movies.append(movie)
        # 영화 Serializer로 직렬화
        serializer = MovieSerializer(recommended_movies, many=True)

        # 결과 딕셔너리 구성
        response_data = {
            "user_liked_genres": user_liked_genres,
            "similarity_res": {movie[0]: movie[1] for movie in top_similar_movies},
            "movie_recommendations": serializer.data
        }

        return Response(response_data)
    else:
        return Response({'error': 'User not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)
    

# 인기도 + 평점 기반 추천
@api_view(['GET'])
def popul_vote_recommend(request):

    developer_preference = {
        'popularity_weight': float(request.GET.get('popularity_weight', 0.1)),
        'vote_average_weight': float(request.GET.get('vote_average_weight', 0.9))
    }

    # 데이터베이스에서 모든 영화 가져오기
    movies = Movie.objects.all()
    scored_movies = []
    print('popularity_weight','vote_average_weight')
    for movie in movies:
        score = personalized_score(movie, developer_preference['popularity_weight'], developer_preference['vote_average_weight'])
        scored_movies.append((movie.title, score, movie))

    scored_movies.sort(key=lambda x: x[1], reverse=True)
    top_scored_movies = scored_movies[:10]

    recommended_movies = [movie[2] for movie in top_scored_movies]
    
    # 영화 Serializer로 직렬화
    serializer = MovieSerializer(recommended_movies, many=True, context={'request': request})

    # 결과 딕셔너리 구성
    response_data = {
        "developer_preference": developer_preference,
        "movie_recommendations": serializer.data
    }

    return Response(response_data)