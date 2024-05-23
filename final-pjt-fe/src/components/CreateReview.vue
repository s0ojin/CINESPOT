<template>
  <div class="border p-6 rounded-lg">
    <h1 v-if="!authLoading && authData" class="text-xl mb-1">
      {{ authData.userInfo.username }}님 이 작품에 대해 어떻게 생각하세요?
    </h1>
    <h1 v-else-if="!authData" class="text-xl mb-1">로그인하고 리뷰 남겨보세요!</h1>
    <StarRating v-model="rating" />
    <textarea
      v-model="content"
      class="input resize-none h-28 pt-2 mt-2"
      placeholder="영화에 대한 감상평이나 기대평을 남겨주세요!"
    ></textarea>
    <button @click="handleSubmit" class="submit-btn w-full h-10 rounded-lg">리뷰 남기기</button>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useMutation, useQueryClient } from '@tanstack/vue-query'
import { postCreateReview } from '@/apis/reviewApi'
import StarRating from '@/components/StarRating.vue'
import { useAuthQuery } from '@/composables/useAuthQuery'

const route = useRoute()
const router = useRouter()
const movieId = route.params.movieId
const queryClient = useQueryClient()

const rating = ref(0)
const content = ref('')

const mutation = useMutation({
  mutationFn: (reviewData) => postCreateReview(movieId, reviewData),
  onSuccess: (data) => {
    queryClient.invalidateQueries(['movieDetails', movieId])
    alert('리뷰작성이 완료되었습니다')
    router.push({ name: 'reviewDetail', params: { reviewId: data.data.id } })
  },
  onError: (error) => {
    if (error.response.status === 401) {
      alert('로그인하고 리뷰를 남길 수 있어요😖!')
    } else alert('리뷰 생성 실패:', error)
  }
})

const { data: authData, isLoading: authLoading } = useAuthQuery()

const handleSubmit = () => {
  const reviewData = {
    content: content.value,
    rating: rating.value
  }
  mutation.mutate(reviewData)
}
</script>
