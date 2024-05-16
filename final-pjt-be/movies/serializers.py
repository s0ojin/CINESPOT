from rest_framework import serializers
from .models import Actor, Movie, Review

class MovieContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ('title',)

class ActorSerializer(serializers.ModelSerializer):
    movies = MovieContentSerializer(source='movie_set', read_only=True, many=True)    

    class Meta:
        model = Actor
        fields = ('id', 'name', 'movies')

class MovieSerialzer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ('title', 'overview')


class ReviewListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ('title', 'content')

class MovieDetailSerializer(serializers.ModelSerializer):
    class ActorNameSerializer(serializers.ModelSerializer):
        class Meta:
            model = Actor
            fields = ('name',)

    actors = ActorNameSerializer(Movie.actors, many=True, read_only=True)
    
    review_set = ReviewListSerializer(Movie.review_set, read_only=True, many=True)

    class Meta:
        model = Movie
        fields = '__all__'


class ReviewDetailSerializer(serializers.ModelSerializer):
    movie = MovieContentSerializer(Review.movie, read_only=True)
    class Meta:
        model = Review
        fields = '__all__'

class ReviewGenSerializer(serializers.ModelSerializer):
    movie = MovieContentSerializer(Review.movie, read_only=True)
    class Meta:
        model = Review
        fields = '__all__'