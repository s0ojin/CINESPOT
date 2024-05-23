#only for recommand system
from accounts.models import User
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# only for recommande system
def compute_cosine_similarity(user_liked_genres, movie_genres):
    # 유저가 좋아요한 장르를 포함한 모든 장르 리스트
    all_genres = user_liked_genres + movie_genres
    
    # 장르 정보를 벡터 형태로 변환
    user_vector = [all_genres.count(genre) for genre in set(all_genres)]  # 사용자 장르 벡터
    movie_vector = [1 if genre in movie_genres else 0 for genre in set(all_genres)]  # 영화 장르 벡터

    # numpy 배열로 변환
    user_array = np.array(user_vector).reshape(1, -1)  # 사용자 벡터를 행 벡터로 변환
    movie_array = np.array(movie_vector).reshape(1, -1)  # 영화 벡터를 행 벡터로 변환

    # 코사인 유사도 계산
    similarity = cosine_similarity(user_array, movie_array)[0][0]

    return similarity
    
# 모든 영화의 장르 정보 가져오기
genres_dict = {
    28: "Action",
    12: "Adventure",
    16: "Animation",
    35: "Comedy",
    80: "Crime",
    99: "Documentary",
    18: "Drama",
    10751: "Family",
    14: "Fantasy",
    36: "History",
    27: "Horror",
    10402: "Music",
    9648: "Mystery",
    10749: "Romance",
    878: "Science Fiction",
    10770: "TV Movie",
    53: "Thriller",
    10752: "War",
    37: "Western"
}


# def personalized_score(movie, popularity_weight, vote_average_weight):
#     score = (movie.popularity * popularity_weight) + (movie.vote_average * vote_average_weight)
#     return score

def personalized_score(movie, popularity_weight, vote_average_weight):
    if popularity_weight > vote_average_weight:
        return movie.popularity
    else:
        return movie.vote_average