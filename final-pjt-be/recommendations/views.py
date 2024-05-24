
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.conf import settings
from openai import OpenAI
import requests

client = OpenAI(
  api_key=settings.OPENAI_API_KEY,
)

@require_GET
def recommend_destinations(request):
    movie_title = request.GET.get('title')
    release_year = request.GET.get('year').strip()
    recommendations = generate_recommendations(movie_title, release_year)
    return JsonResponse(recommendations, json_dumps_params={'ensure_ascii': False})

def generate_recommendations(movie_title, release_year):
    recommended_destinations = []
    recommendations = {
        "movie_title": movie_title,
        "release_year": release_year,
        "recommended_destinations": recommended_destinations,
    }
    for i in range(2):
        first_prompt = f"영화 '{movie_title}'(출시 연도: {release_year})의 여행지 추천. 목적지 이름 정확히 하나만 알려줘"
        if i > 0:
            first_prompt = f"영화 '{movie_title}'(출시 연도: {release_year})의 여행지로 {destination}을 추천 받았어. 다른 목적지 정확히 하나만 추천해줘"
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a travel recommendation assistant. you should say exact words only."},
                {"role": "user", "content": first_prompt}
            ]
        )
        destination = response.to_dict()['choices'][0]['message']['content']

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a travel recommendation assistant. you should say exact words only."},
                {"role": "user", "content": f"영화 '{movie_title}'(출시 연도: {release_year})의 여행지로 {destination}을 추천 받았어. 이걸 추천한 적절한 이유 알려줘."}
            ]
        )
        reason = response.to_dict()['choices'][0]['message']['content']

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a travel recommendation assistant. you should say exact words only."},
                {"role": "user", "content": f"영화 '{movie_title}'(출시 연도: {release_year})의 여행지로 {destination}을 추천 받았어. 여기 정확한 주소 알려줘"}
            ]
        )
        address = response.to_dict()['choices'][0]['message']['content']
        image = get_top_image_url(destination+" 풍경")
        recommended_destinations.append({
            "destination": destination,
            "reason": reason,
            "address": address,
            "image_url": image
        })
    return recommendations

def get_top_image_url(search_term):
    google_image_search_api_key = settings.GOOGLE_API_KEY
    google_cse_id = "629ce138107d84d93"
    cse_id = google_cse_id
    api_key = google_image_search_api_key

    service_url = 'https://www.googleapis.com/customsearch/v1'
    params = {
        'q': search_term,
        'key': api_key,
        'cx': cse_id,
        'searchType': 'image',
        'num': 1,  # 검색 결과의 수 (최상위 1개)
    }

    # API 요청
    response = requests.get(service_url, params=params)
    result = response.json()

    # 최상위 이미지 URL 반환
    if 'items' in result:
        return result['items'][0]['link']
    else:
        return None