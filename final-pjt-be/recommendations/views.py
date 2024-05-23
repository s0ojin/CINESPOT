
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.conf import settings

from openai import OpenAI

client = OpenAI(
  api_key=settings.OPENAI_API_KEY,
)

@require_GET
def recommend_destinations(request):
    movie_title = request.GET.get('title')
    release_year = request.GET.get('year').strip()

    recommendations = generate_recommendations(movie_title, release_year)

    return JsonResponse(recommendations)

def generate_recommendations(movie_title, release_year):
    prompt = f"영화 '{movie_title}'(출시 연도: {release_year})의 여행지 추천. 목적지, 이유, 주소, 이미지 URL 포함."

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a travel recommendation assistant."},
            {"role": "user", "content": prompt}
        ]
    )

    response_text = response.to_dict()['choices'][0]['message']['content']
    print(response.to_dict()['choices'][0]['message']['content'])

    recommendations = {
        "movie_title": movie_title,
        "release_year": release_year,
        "recommended_destinations": []
    }

    # 응답 텍스트를 개행 문자로 분리하고 각 여행지 정보 추출
    entries = response_text.split("\n\n")
    for entry in entries:
        lines = entry.split("\n")
        if len(lines) > 1:  # 여행지 정보가 최소 2줄 이상 있는 경우
            destination_info = lines[1].split("-")  # 첫 번째 줄은 목적지 제목, 두 번째 줄은 상세 정보
            if len(destination_info) >= 4:
                destination = lines[0].strip().split(".")[1].strip()  # "1. **로스앤젤레스, 미국**" 형식 처리
                reason = destination_info[1].strip()
                address = destination_info[2].strip()
                image_url = destination_info[3].strip().split(" ")[-1][1:-1]  # 마크다운 링크에서 URL 추출
                recommendations["recommended_destinations"].append({
                    "destination": destination,
                    "reason": reason,
                    "address": address,
                    "image_url": image_url
                })

    return recommendations
