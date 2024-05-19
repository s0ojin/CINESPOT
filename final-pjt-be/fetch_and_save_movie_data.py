import requests
import os
import django
import sys
import json

# Django settings 모듈을 불러와서 설정값들을 사용할 수 있도록 설정
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "final_pjt.settings")
django.setup()

from django.conf import settings
from movies.models import Movie

def fetch_movie_data(movie_id):
    api_key = settings.TMDB_API_KEY  # 실제 API 키로 변경하세요
    url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}'

    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f'Failed to fetch movie data for movie ID {movie_id}:', response.status_code)
        return None

def save_movie_data_to_db(movie_data):
    movie, created = Movie.objects.update_or_create(
        id=movie_data['id'],
        defaults={
            'title': movie_data.get('title', ''),
            'overview': movie_data.get('overview', ''),
            'release_date': movie_data.get('release_date', None),
            'vote_average': movie_data.get('vote_average', None),
            'vote_count': movie_data.get('vote_count', None),
            'popularity': movie_data.get('popularity', None),
            'poster_path': movie_data.get('poster_path', ''),
            # 'backdrop_path': movie_data.get('backdrop_path', ''),
            # 'original_language': movie_data.get('original_language', ''),
            'genre_ids': movie_data.get('genre_ids', []),
            # 'raw_data': movie_data  # 모든 데이터를 저장
        }
    )
    return movie

def save_movies_to_json(movies_data, filename='movies_fixture.json'):
    fixture_format = [
        {
            "model": "movies.Movie",
            "pk": movie_data['id'],
            "fields": movie_data  # 모든 데이터를 저장
        } for movie_data in movies_data if movie_data
    ]

    # Django 프로젝트 폴더 기준으로 경로 설정
    fixtures_dir = os.path.join(settings.BASE_DIR, 'movies', 'fixtures')
    os.makedirs(fixtures_dir, exist_ok=True)
    with open(os.path.join(fixtures_dir, filename), 'w', encoding='utf-8') as f:
        json.dump(fixture_format, f, ensure_ascii=False, indent=4)
    print(f'Successfully saved data to {filename}')

if __name__ == "__main__":
    movies_data = []
    movie_id = 1

    while len(movies_data) < 10:
        movie_data = fetch_movie_data(movie_id)
        if movie_data:
            movie = save_movie_data_to_db(movie_data)
            movies_data.append(movie_data)
            print(f'Successfully fetched and saved data for movie ID {movie_id}')
        movie_id += 1

    save_movies_to_json(movies_data)
    print(f'Successfully fetched and saved data for {len(movies_data)} movies')
