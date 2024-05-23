<template>
  <div class="max-w-4xl mx-auto">
    <div v-if="isLoading">Loading review...</div>
    <div v-if="error">Error loading review: {{ error.message }}</div>
    <div v-if="!isLoading && !error && review">
      <div class="flex items-center relative">
        <img :src="review.authorInfo.authorProfile" alt="Author Avatar" class="h-10 w-10 rounded-full mr-2" />
        <div>
          <p class="font-semibold">{{ review.authorInfo.author }}</p>
          <p class="text-sm text-slate-600">{{ getConvertedTime(review.created_at) }}</p>
        </div>
        <button @click="toggleDropdown(true)" class="pi pi-ellipsis-v p-2 pr-0 text-md text-slate-500 ml-auto"></button>
        <div
          ref="dropdown"
          v-if="isDropdownVisible"
          class="absolute right-0 mt-2 w-40 bg-white border rounded shadow-md z-10"
        >
          <ul>
            <li @click="confirmDelete" class="px-4 py-2 hover:bg-gray-100 cursor-pointer">삭제하기</li>
            <li @click="goToReviewEdit" class="px-4 py-2 hover:bg-gray-100 cursor-pointer">수정하기</li>
          </ul>
        </div>
      </div>

      <div>
        <div
          class="flex h-32 gap-4 p-4 pr-8 my-4 border rounded-xl hover:bg-slate-50 transition cursor-pointer"
          @click="handleToMovieDetail"
        >
          <img
            :src="`https://image.tmdb.org/t/p/w500${review.movieInfo.poster_path}`"
            alt="Poster"
            class="rounded-lg border object-cover"
          />
          <div class="flex w-full justify-between items-center">
            <div>
              <h2>
                {{ review.movieInfo.title }}
              </h2>
              <div class="flex gap-2 text-sm text-slate-600">
                <span>{{ review.movieInfo.release_date.split('-')[0] }}</span>
                <span class="leading-3">.</span>
                <span>{{ getCountryNameInKorean(review.movieInfo.production_countries[0].iso_3166_1) }}</span>
                <span class="leading-3">.</span>
                <span>{{ review.movieInfo.runtime }}분</span>
              </div>
              <div class="flex gap-2 flex-wrap mt-2 text-sm">
                <span v-for="(genre, idx) in review.movieInfo.genres" :key="idx" class="border py-1 px-2 rounded-2xl">{{
                  genre
                }}</span>
              </div>
            </div>
            <div class="flex items-center">
              <span class="mr-2">{{ review.rating }}</span>
              <div class="flex">
                <i v-for="i in 5" :key="i" class="text-yellow-500 relative">
                  <i v-if="getStarStatus(review.rating, i) === 'half'">
                    <svg
                      xmlns="http://www.w3.org/2000/svg"
                      viewBox="0 0 576 512"
                      class="w-[18px] fill-yellow-500 mt-[3px]"
                      fill="current"
                    >
                      <path
                        d="M309.5 13.5C305.5 5.2 297.1 0 287.9 0s-17.6 5.2-21.6 13.5L197.7 154.8 44.5 177.5c-9 1.3-16.5 7.6-19.3 16.3s-.5 18.1 5.9 24.5L142.2 328.4 116 483.9c-1.5 9 2.2 18.1 9.7 23.5s17.3 6 25.3 1.7l137-73.2 137 73.2c8.1 4.3 17.9 3.7 25.3-1.7s11.2-14.5 9.7-23.5L433.6 328.4 544.8 218.2c6.5-6.4 8.7-15.9 5.9-24.5s-10.3-14.9-19.3-16.3L378.1 154.8 309.5 13.5zM288 384.7V79.1l52.5 108.1c3.5 7.1 10.2 12.1 18.1 13.3l118.3 17.5L391 303c-5.5 5.5-8.1 13.3-6.8 21l20.2 119.6L299.2 387.5c-3.5-1.9-7.4-2.8-11.2-2.8z"
                      />
                    </svg>
                  </i>
                  <i :class="getStarStatus(review.rating, i)"></i>
                </i>
              </div>
            </div>
          </div>
        </div>

        <div class="p-2 pt-4">
          <p class="text-slate-800 pb-8">{{ review.content }}</p>

          <div class="flex justify-end mt-2 items-center gap-4 text-slate-700">
            <button @click="toggleLike">
              <i
                :class="[
                  'pi',
                  review.is_liked ? 'pi-thumbs-up-fill' : 'pi-thumbs-up',
                  review.is_liked && 'text-primary-500'
                ]"
              ></i>
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
        <div
          @click="hideDeleteModal"
          v-if="isDeleteModalVisible"
          class="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50"
        >
          <div class="bg-white p-6 rounded shadow-lg">
            <p class="mb-4">정말 리뷰를 삭제할까요?</p>
            <div class="flex gap-2 w-full">
              <button @click="hideDeleteModal" class="py-2 w-full bg-slate-200 rounded">취소</button>
              <button @click="handleDeleteReview" class="py-2 w-full bg-red-500 text-white rounded">삭제</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { getCountryNameInKorean } from '@/utils/convertCountryName'
import { useRoute, useRouter } from 'vue-router'
import CommentCard from '@/components/CommentCard.vue'
import { getConvertedTime } from '@/utils/convertTime.js'
import { useMutation, useQuery, useQueryClient } from '@tanstack/vue-query'
import { deleteReview, getReviewDetail, postCreateComment, postReviewLike } from '@/apis/reviewApi'
import { getStarStatus } from '@/utils/getStarStatus'

const router = useRouter()
const route = useRoute()
const reviewId = route.params.reviewId
const queryClient = useQueryClient()

const {
  data: review,
  error,
  isLoading
} = useQuery({
  queryKey: ['reviewDetail', reviewId],
  queryFn: () => getReviewDetail(reviewId).then((res) => res.data)
})

const commentMutation = useMutation({
  mutationFn: (commentData) => postCreateComment(reviewId, commentData),
  onSuccess: () => {
    queryClient.invalidateQueries(['reviewDetail', reviewId])
  },
  onError: (error) => {
    alert('댓글 생성 실패:', error)
  }
})

const reviewDeleteMutation = useMutation({
  mutationFn: (reviewId) => deleteReview(reviewId),
  onSuccess: () => {
    alert('리뷰가 삭제되었습니다.')
    router.push({ name: 'movieReviewList', params: { movieId: review.value.movieInfo.id } })
    queryClient.invalidateQueries(['movieDetails', review.value.movieInfo.id])
    queryClient.invalidateQueries(['movieReviews'])
  }
})

const reviewLikeMutation = useMutation({
  mutationFn: (reviewId) => postReviewLike(reviewId),
  onSuccess: () => {
    queryClient.invalidateQueries(['reviewDetail', reviewId])
  },
  onError: (err) => {
    if (err.response.status === 403) {
      alert('자신의 리뷰에 좋아요를 누를 수 없어요!😜')
    }
  }
})

const newComment = ref('')

const toggleLike = () => {
  reviewLikeMutation.mutate(reviewId)
}

const addComment = () => {
  if (newComment.value.trim()) {
    commentMutation.mutate({ content: newComment.value })
    newComment.value = ''
  }
}

const handleToMovieDetail = () => {
  router.push({ name: 'movieDetail', params: { movieId: review.value.movieInfo.id } })
}

const isDropdownVisible = ref(false)
const isDeleteModalVisible = ref(false)

const toggleDropdown = (boolean) => {
  isDropdownVisible.value = boolean
}

const handleDeleteReview = () => {
  reviewDeleteMutation.mutate(reviewId)
}

const confirmDelete = () => {
  isDropdownVisible.value = false
  isDeleteModalVisible.value = true
}

const hideDeleteModal = () => {
  isDeleteModalVisible.value = false
}

const goToReviewEdit = () => {
  router.push({ name: 'reviewUpdate', params: { reviewId: reviewId } })
}
</script>
