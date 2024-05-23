<template>
  <div>
    <div v-if="comments.length === 0" class="text-center py-10">아직 댓글 없습니다...😔<br /></div>
    <div v-for="(comment, idx) in comments" :key="comment.id" class="mb-4 relative">
      <div class="flex gap-4 items-start px-2">
        <img src="https://via.placeholder.com/50" alt="Commenter Avatar" class="h-8 w-8 rounded-full" />
        <div class="flex-1">
          <div class="flex justify-between items-end mb-2">
            <p class="font-semibold">{{ comment.authorInfo.author }}</p>
            <p class="text-sm text-slate-500">{{ getConvertedTime(comment.created_at) }}</p>
          </div>
          <p class="text-gray-800">{{ comment.content }}</p>
        </div>
        <button @click="toggleDropdown(comment.id)" class="pi pi-ellipsis-v p-2 pr-0 text-xs text-slate-500"></button>
        <div
          ref="dropdown"
          v-if="isDropdownVisible && activeCommentId === comment.id"
          class="absolute right-0 mt-2 w-40 bg-white border rounded shadow-md z-10"
        >
          <ul>
            <li @click="confirmDelete(comment.id)" class="px-4 py-2 hover:bg-gray-100 cursor-pointer">삭제하기</li>
          </ul>
        </div>
      </div>
      <hr v-if="idx !== comments.length - 1" class="my-3" />
    </div>

    <!-- 삭제 확인 모달 -->
    <div
      @click="hideModal"
      v-if="isModalVisible"
      class="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50"
    >
      <div class="bg-white p-6 rounded shadow-lg">
        <p class="mb-4">정말 댓글을 삭제할까요?</p>
        <div class="flex gap-2 w-full">
          <button @click="hideModal" class="py-2 w-full bg-slate-200 rounded">취소</button>
          <button @click="handleDeleteComment" class="py-2 w-full bg-red-500 text-white rounded">삭제</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { getConvertedTime } from '@/utils/convertTime.js'
import { useMutation, useQueryClient } from '@tanstack/vue-query'
import { deleteComment } from '@/apis/reviewApi'
import { useRoute } from 'vue-router'
import { onClickOutside } from '@vueuse/core'

defineProps({
  comments: {
    type: Array,
    required: true
  }
})
const queryClient = useQueryClient()
const route = useRoute()
const reviewId = route.params.reviewId

const commentMutation = useMutation({
  mutationFn: (commentId) => deleteComment(commentId),
  onSuccess: () => {
    queryClient.invalidateQueries(['reviewDetail', reviewId])
  },
  onError: (error) => {
    alert('댓글 삭제 실패:', error)
  }
})

const isDropdownVisible = ref(false)
const activeCommentId = ref(null)
const isModalVisible = ref(false)
const targetCommentId = ref(null)

const dropdown = ref(null)
onClickOutside(dropdown, () => toggleDropdown(false))

const toggleDropdown = (commentId) => {
  if (activeCommentId.value === commentId) {
    isDropdownVisible.value = !isDropdownVisible.value
  } else {
    activeCommentId.value = commentId
    isDropdownVisible.value = true
  }
}

const confirmDelete = (commentId) => {
  targetCommentId.value = commentId
  isDropdownVisible.value = false
  isModalVisible.value = true
}

const hideModal = () => {
  isModalVisible.value = false
  targetCommentId.value = null
}

const handleDeleteComment = () => {
  if (targetCommentId.value !== null) {
    commentMutation.mutate(targetCommentId.value)
    hideModal()
  }
}
</script>
