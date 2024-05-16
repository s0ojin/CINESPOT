from django.shortcuts import render, get_object_or_404
from .models import Actor, Movie, Review
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import ActorSerializer, MovieSerialzer, MovieDetailSerializer, ReviewListSerializer, ReviewDetailSerializer, ReviewGenSerializer

# Create your views here.

@api_view(['GET'])
def movie_list(request):
    movies = Movie.objects.all()
    serialzer = MovieSerialzer(movies, many=True)
    return Response(serialzer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def movie_detail(request,movie_pk): # 단일 영화 정보 제공 (출연 배우 목록+리뷰 목록)
    # 감독 이름도 추가하려면 movie 모델에 감독 필드 선언하믄 되지 않나여
    movie= Movie.objects.get(pk=movie_pk)
    serializer = MovieDetailSerializer(movie)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def review_list(request): # 리뷰 리스트 -> 댓글 리스트
    reviews = Review.objects.all()
    serializer = ReviewListSerializer(reviews, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET', 'PUT', 'DELETE'])
def review_detail(request, review_pk): # 단일 리뷰 조회&수정&삭제를 댓글로 바꾸기
    review = Review.objects.get(pk=review_pk)
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
def create_review(request, movie_pk): # 리뷰 생성을 댓글 생성으로 바꾸기
    # movie = Movie.objects.get(pk=movie_pk)
    movie = get_object_or_404(Movie, pk=movie_pk)
    serializer = ReviewGenSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save(movie=movie)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
