import requests
import os
import django
import json

# Django settings 모듈을 불러와서 설정값들을 사용할 수 있도록 설정
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "final_pjt.settings")
django.setup()

from django.conf import settings
from movies.models import Movie

def fetch_genres():
    api_key = settings.TMDB_API_KEY
    genres_url = f'https://api.themoviedb.org/3/genre/movie/list?api_key={api_key}&language=en-US'
    
    response = requests.get(genres_url)
    if response.status_code == 200:
        genres_data = response.json()
        return {genre['id']: genre['name'] for genre in genres_data['genres']}
    else:
        print(f'Failed to fetch genres: {response.status_code}')
        return {}

def fetch_movie_data(movie_id, genre_dict):
    api_key = settings.TMDB_API_KEY
    movie_url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}'
    images_url = f'https://api.themoviedb.org/3/movie/{movie_id}/images?api_key={api_key}'

    movie_response = requests.get(movie_url)
    images_response = requests.get(images_url)
    
    if movie_response.status_code == 200 and images_response.status_code == 200:
        movie_data = movie_response.json()
        images_data = images_response.json()
        still_cut_paths = [img['file_path'] for img in images_data.get('backdrops', [])]
        movie_data['still_cut_paths'] = still_cut_paths
        
        # Convert genres field to genre_ids
        movie_data['genre_ids'] = [genre['id'] for genre in movie_data.get('genres', [])]
        movie_data['genres'] = [genre_dict[genre['id']] for genre in movie_data.get('genres', [])]
        return movie_data
    else:
        print(f'Failed to fetch movie data for movie ID {movie_id}:', movie_response.status_code, images_response.status_code)
        return None

def save_movie_data_to_db(movie_data):
    movie, created = Movie.objects.update_or_create(
        id=movie_data['id'],
        defaults={
            'title': movie_data.get('title', ''),
            'overview': movie_data.get('overview', ''),
            'release_date': movie_data.get('release_date', None),
            'poster_path': movie_data.get('poster_path', ''),
            'backdrop_path': movie_data.get('backdrop_path', ''),
            'genre_ids': movie_data.get('genre_ids', []),
            'genres': movie_data.get('genres', []),  # 장르 이름 저장
            'production_countries': movie_data.get('production_countries', []),
            'still_cut_paths': movie_data.get('still_cut_paths', []),
            'runtime': movie_data.get('runtime', None),
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
    genre_dict = fetch_genres()
    movies_data = []
    movie_id = 1

    while len(movies_data) < 50:
        movie_data = fetch_movie_data(movie_id, genre_dict)
        if movie_data:
            movie = save_movie_data_to_db(movie_data)
            movies_data.append(movie_data)
            print(f'Successfully fetched and saved data for movie ID {movie_id}')
        movie_id += 1

    save_movies_to_json(movies_data)
    print(f'Successfully fetched and saved data for {len(movies_data)} movies')
