<template>
  <div class="max-w-4xl mx-auto">
    <div v-if="isLoading">Loading review...</div>
    <div v-if="error">Error loading review: {{ error.message }}</div>
    <div v-if="!isLoading && !error">
      <div class="flex items-center">
        <img :src="review.profileImage" alt="Author Avatar" class="h-10 w-10 rounded-full mr-2" />
        <div>
          <p class="font-semibold">{{ review.author }}</p>
          <p class="text-sm text-slate-600">{{ getConvertedTime(review.created_at) }}</p>
        </div>
        <button @click="toggleDropdown()" class="pi pi-ellipsis-v p-2 pr-0 text-md text-slate-500 ml-auto"></button>
        <div v-if="isDropdownVisible" class="absolute right-0 mt-2 w-40 bg-white border rounded shadow-md z-10">
          <ul>
            <li @click="confirmDelete(review.id)" class="px-4 py-2 hover:bg-gray-100 cursor-pointer">삭제하기</li>
            <li @click="editReview(review.id)" class="px-4 py-2 hover:bg-gray-100 cursor-pointer">수정하기</li>
          </ul>
        </div>
      </div>

      <div
        class="flex h-32 gap-4 p-4 pr-8 my-4 border rounded-xl hover:bg-slate-50 transition cursor-pointer"
        @click="handleToMovieDetail"
      >
        <img
          :src="`https://image.tmdb.org/t/p/w500${review.movie.poster_path}`"
          alt="Poster"
          class="rounded-lg border object-cover"
        />
        <div class="flex w-full justify-between items-center">
          <div>
            <h2>
              {{ review.movie.title }}
            </h2>
            <div class="flex gap-2 text-sm text-slate-600">
              <span>{{ review.movie.release_date.split('-')[0] }}</span>
              <span class="leading-3">.</span>
              <span>{{ getCountryNameInKorean(review.movie.production_country) }}</span>
              <span class="leading-3">.</span>
              <span>{{ review.movie.runtime }}분</span>
            </div>
            <div class="flex gap-2 flex-wrap mt-2 text-sm">
              <span v-for="genre in review.movie.genre_ids" :key="genre.id" class="border py-1 px-2 rounded-2xl">{{
                genre.name
              }}</span>
            </div>
          </div>
          <div class="flex flex-col items-center">
            <p class="text-xl">{{ review.score }}</p>
            <div class="flex">
              <i v-for="i in 5" :key="i" class="text-yellow-500">
                <i :class="i <= review.score / 2 ? 'pi pi-star-fill' : 'pi pi-star'"></i>
              </i>
            </div>
          </div>
        </div>
      </div>

      <div class="p-2 pt-4">
        <p class="text-slate-800 pb-8">{{ review.content }}</p>

        <div class="flex justify-end mt-2 items-center gap-4 text-slate-700">
          <button @click="toggleLike" :class="{ 'text-primary-500': liked }">
            <i :class="[liked ? 'pi pi-thumbs-up-fill' : 'pi pi-thumbs-up']"></i>
            <span class="ml-2">{{ review.likes_count }}</span>
          </button>
          <div>
            <i class="pi pi-comment"></i>
            <span class="ml-1">{{ review.comments.length }}</span>
          </div>
        </div>
      </div>
      <hr class="p-2" />

      <CommentCard :comments="review.comments" />

      <div class="mt-14 flex gap-4 items-end">
        <textarea
          v-model="newComment"
          placeholder="이 리뷰에 대해 어떻게 생각하시나요? 댓글로 소통해보세요!"
          class="input h-20 px-3 py-2"
        ></textarea>
        <button
          @click="addComment"
          class="pi pi-arrow-circle-right mb-1 text-3xl text-slate-400 hover:text-primary-500"
        ></button>
      </div>

      <!-- 삭제 확인 모달 -->
      <div v-if="isModalVisible" class="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50">
        <div class="bg-white p-6 rounded shadow-lg">
          <p class="mb-4">정말 리뷰를 삭제할까요?</p>
          <div class="flex gap-2 w-full">
            <button @click="hideModal" class="py-2 w-full bg-slate-200 rounded">취소</button>
            <button @click="deleteReview" class="py-2 w-full bg-red-500 text-white rounded">삭제</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getCountryNameInKorean } from '@/utils/convertCountryName'
import { useRouter } from 'vue-router'
import CommentCard from '@/components/CommentCard.vue'
import { getConvertedTime } from '@/utils/convertTime.js'

const router = useRouter()

// 더미 데이터
const review = ref(null)
const isLoading = ref(true)
const error = ref(null)

const dummyReviewDetail = {
  movie: {
    id: 5,
    title: '인셉션',
    poster_path: '/3rvvpS9YPM5HB2f4HYiNiJVtdam.jpg',
    production_country: 'US',
    release_date: '2010-07-16',
    genre_ids: [
      { id: 1, name: '코미디' },
      { id: 2, name: 'SF' }
    ],
    runtime: 100
  },
  id: 1,
  author: '박수진차진차',
  content:
    '이 영화 진짜 너무 너무 너문 ㅁ눔 내스타일 취저 너무 재밌어 인생영화이 영화 진짜 너무 너무 너문 ㅁ눔 내스타일 취저 너무 재밌어 인생영화이 영화 진짜 너무 너무 너문 ㅁ눔 내스타일 취저 너무 재밌어 인생영화이 영화 진짜 너무 너무 너문 ㅁ눔 내스타일 취저 너무 재밌어 인생영화이 영화 진짜 너무 너무 너문 ㅁ눔 내스타일 취저 너무 재밌어 인생영화',
  profileImage: 'https://via.placeholder.com/150',
  created_at: '2023-05-01T12:34:56Z',
  updated_at: '2023-05-02T14:23:45Z',
  likes_count: 120,
  score: 3.5,
  comments: [
    {
      id: 1,
      created_at: '2024-05-21T12:34:56Z',
      author: '박경령차영차',
      content:
        '저는 이영화가 개쓰레기라고 생각해요.저는 이영화가 개쓰레기라고 생각해요.저는 이영화가 개쓰레기라고 생각해요.저는 이영화가 개쓰레기라고 생각해요.저는 이영화가 개쓰레기라고 생각해요.저는 이영화가 개쓰레기라고 생각해요.저는 이영화가 개쓰레기라고 생각해요.저는 이영화가 개쓰레기라고 생각해요.'
    },
    {
      id: 2,
      author: 'Bob Johnson',
      created_at: '2023-05-01T12:34:56Z',
      content: 'A masterpiece by Christopher Nolan. A must-watch!'
    }
  ]
}

onMounted(() => {
  setTimeout(() => {
    review.value = dummyReviewDetail
    isLoading.value = false
  }, 1000)
})

const likes = ref(review.value?.likes_count)
const liked = ref(false)
const newComment = ref('')

const toggleLike = () => {
  liked.value = !liked.value
  likes.value += liked.value ? 1 : -1
}

const addComment = () => {
  if (newComment.value.trim()) {
    review.value.comments.push({
      id: review.value.comments.length + 1,
      author: 'New User', // 실제로는 로그인된 사용자 정보 사용
      content: newComment.value.trim()
    })
    newComment.value = ''
  }
}

const handleToMovieDetail = () => {
  router.push({ name: 'movieDetail', params: { movieId: review.value.movie.id } })
}

const isDropdownVisible = ref(false)
const isModalVisible = ref(false)
const commentToDelete = ref(null)

const toggleDropdown = () => {
  isDropdownVisible.value = true
}

const deleteReview = () => {
  if (commentToDelete.value !== null) {
    // props.comments = props.comments.filter((comment) => comment.id !== commentToDelete.value)
    hideModal()
  }
}

const confirmDelete = (reviewId) => {
  commentToDelete.value = reviewId
  isDropdownVisible.value = false
  isModalVisible.value = true
}

const editReview = (reviewId) => {
  console.log(`Editing comment with id: ${reviewId}`)
  isDropdownVisible.value = false
}

const hideModal = () => {
  isModalVisible.value = false
  commentToDelete.value = null
}
</script>
