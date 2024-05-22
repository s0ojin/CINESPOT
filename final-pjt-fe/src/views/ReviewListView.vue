<template>
  <div class="flex flex-col gap-4 max-w-4xl mx-auto">
    <div
      class="flex h-72 gap-4 p-4 pr-8 my-4 border rounded-xl hover:bg-slate-50 transition cursor-pointer"
      @click="handleToMovieDetail"
    >
      <img
        :src="`https://image.tmdb.org/t/p/w500${movie.poster_path}`"
        alt="Poster"
        class="rounded-lg border object-cover w-44"
      />

      <div class="flex flex-col p-2">
        <h2 class="text-xl">{{ movie.title }}</h2>
        <div class="flex gap-2 text-sm text-slate-600">
          <span>{{ movie.release_date.split('-')[0] }}</span>
          <span class="leading-3">.</span>
          <span>{{ getCountryNameInKorean(movie.production_country) }}</span>
          <span class="leading-3">.</span>
          <span>{{ movie.runtime }}분</span>
        </div>
        <p class="flex-1 mt-4">{{ movie.overview }}</p>
        <div class="flex gap-2 flex-wrap text-sm mt-auto">
          <span v-for="genre in movie.genre_ids" :key="genre.id" class="border py-1 px-2 rounded-2xl">{{
            genre.name
          }}</span>
        </div>
      </div>
    </div>
    <div v-if="reviews.length > 0" class="grid grid-cols-1 gap-3 mt-4">
      <div v-for="review in reviews" :key="review.id">
        <reviewCard :review="review" :contentLimit="200" />
      </div>
    </div>
  </div>
</template>

<script setup>
import ReviewCard from '@/components/reviewCard.vue'

const movie = {
  poster_path: '/3rvvpS9YPM5HB2f4HYiNiJVtdam.jpg',
  title: '더미 영화 제목',
  release_date: '2023-01-01',
  production_country: 'US',
  runtime: 120,
  genre_ids: [
    { id: 1, name: '드라마' },
    { id: 2, name: '코미디' }
  ],
  overview:
    '이 영화 마지막에 주인공 죽음이 영화 마지막에 주인공 죽음이 영화 마지막에 주인공 죽음이 영화 마지막에 주인공 죽음이 영화 마지막에 주인공 죽음이 영화 마지막에 주인공 죽음이 영화 마지막에 주인공 죽음이 영화 마지막에 주인공 죽음이 영화 마지막에 주인공 죽음이 영화 마지막에 주인공 죽음이 영화 마지막에 주인공 죽음'
}

const reviews = [
  {
    id: 1,
    score: 8,
    author: '사용자1',
    authorProfile: '/path_to_profile1.jpg',
    content:
      '이 영화는 정말 훌륭합니다. 배우들의 연기가 인상적이었고, 스토리가 매우 흥미로웠습니다. 강력 추천합니다!이 영화는 정말 훌륭합니다. 배우들의 연기가 인상적이었고, 스토리가 매우 흥미로웠습니다. 강력 추천합니다!이 영화는 정말 훌륭합니다. 배우들의 연기가 인상적이었고, 스토리가 매우 흥미로웠습니다. 강력 추천합니다!이 영화는 정말 훌륭합니다. 배우들의 연기가 인상적이었고, 스토리가 매우 흥미로웠습니다. 강력 추천합니다!이 영화는 정말 훌륭합니다. 배우들의 연기가 인상적이었고, 스토리가 매우 흥미로웠습니다. 강력 추천합니다!이 영화는 정말 훌륭합니다. 배우들의 연기가 인상적이었고, 스토리가 매우 흥미로웠습니다. 강력 추천합니다!이 영화는 정말 훌륭합니다. 배우들의 연기가 인상적이었고, 스토리가 매우 흥미로웠습니다. 강력 추천합니다!이 영화는 정말 훌륭합니다. 배우들의 연기가 인상적이었고, 스토리가 매우 흥미로웠습니다. 강력 추천합니다!이 영화는 정말 훌륭합니다. 배우들의 연기가 인상적이었고, 스토리가 매우 흥미로웠습니다. 강력 추천합니다!이 영화는 정말 훌륭합니다. 배우들의 연기가 인상적이었고, 스토리가 매우 흥미로웠습니다. 강력 추천합니다!이 영화는 정말 훌륭합니다. 배우들의 연기가 인상적이었고, 스토리가 매우 흥미로웠습니다. 강력 추천합니다!',
    likes: 10,
    liked: false,
    comments: []
  },
  {
    id: 2,
    score: 6,
    author: '사용자2',
    authorProfile: '/path_to_profile2.jpg',
    content: '나쁘지 않았지만, 약간 지루한 부분이 있었습니다. 그래도 전체적으로 볼 만한 영화였습니다.',
    likes: 5,
    liked: false,
    comments: [{ id: 3, content: '동의합니다. 저도 그렇게 느꼈어요.' }]
  },
  {
    id: 3,
    score: 9,
    author: '사용자3',
    authorProfile: '/path_to_profile3.jpg',
    content: '이 영화는 정말 최고입니다. 다시 보고 싶어요!',
    likes: 20,
    liked: false,
    comments: []
  }
]

const handleToMovieDetail = () => {
  // 상세 페이지로 이동하는 로직
}

const getCountryNameInKorean = (countryCode) => {
  // 국가 코드를 한국어로 변환하는 로직
}
</script>
