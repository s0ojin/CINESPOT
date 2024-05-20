from django.shortcuts import get_object_or_404
from .models import Movie, Review, Review_likes_users
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .serializers import MovieSerialzer, MovieDetailSerializer, ReviewListSerializer, ReviewDetailSerializer, ReviewGenSerializer

# Create your views here.

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
    serialzer = MovieSerialzer(movies, many=True)
    return Response(serialzer.data, status=status.HTTP_200_OK)

# 영화 상세 내역 조회 원본 코드
@api_view(['GET'])
def movie_detail(request,movie_pk):
    movie= Movie.objects.get(pk=movie_pk)
    serializer = MovieDetailSerializer(movie)
    return Response(serializer.data, status=status.HTTP_200_OK)
# @api_view(['GET'])
# def movie_detail(request, movie_pk):
#     movie = get_object_or_404(Movie, pk=movie_pk)
#     serializer = MovieDetailSerializer(movie)
#     return Response(serializer.data)



# 리뷰 목록 조회 뷰함수
@api_view(['GET'])
def review_list(request):
    reviews = Review.objects.all()
    serializer = ReviewListSerializer(reviews, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET', 'PUT', 'DELETE'])
def review_detail(request, review_pk):
    review = Review.objects.get(pk=review_pk)
    # review = get_object_or_404(Review, pk=review_pk)
    if request.method == 'GET':
        serializer = ReviewDetailSerializer(review)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    elif request.method == 'PUT':
        serializer = ReviewDetailSerializer(review, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
    elif request.method == 'DELETE':
        review.delete()
        return Response({'message': f'review {review_pk} is deleted.'}, status=status.HTTP_204_NO_CONTENT)
    
@api_view(['POST'])
def create_review(request, movie_pk):
    # movie = Movie.objects.get(pk=movie_pk)
    movie = get_object_or_404(Movie, pk=movie_pk)
    serializer = ReviewGenSerializer(data=request.data,  context={'request': request, 'movie': movie})
    if serializer.is_valid(raise_exception=True):
        serializer.save(movie=movie)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
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

    # Review_likes_users 모델을 사용하여 좋아요 추가/삭제
    review_like, created = Review_likes_users.objects.get_or_create(review=review, user=user)

    if not created:
        review_like.delete()
        liked = False
    else:
        liked = True

    return Response({'liked': liked, 'like_count': review.likes.count()}, status=status.HTTP_200_OK)
