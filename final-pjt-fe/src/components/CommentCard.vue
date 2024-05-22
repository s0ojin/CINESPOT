<template>
  <div>
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
    <div v-if="isModalVisible" class="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50">
      <div class="bg-white p-6 rounded shadow-lg">
        <p class="mb-4">정말 댓글을 삭제할까요?</p>
        <div class="flex gap-2 w-full">
          <button @click="hideModal" class="py-2 w-full bg-slate-200 rounded">취소</button>
          <button @click="deleteComment" class="py-2 w-full bg-red-500 text-white rounded">삭제</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { getConvertedTime } from '@/utils/convertTime.js'

defineProps({
  comments: {
    type: Array,
    required: true
  }
})

const isDropdownVisible = ref(false)
const activeCommentId = ref(null)
const isModalVisible = ref(false)
const commentToDelete = ref(null)

const toggleDropdown = (commentId) => {
  if (activeCommentId.value === commentId) {
    isDropdownVisible.value = !isDropdownVisible.value
  } else {
    activeCommentId.value = commentId
    isDropdownVisible.value = true
  }
}

const confirmDelete = (commentId) => {
  commentToDelete.value = commentId
  isDropdownVisible.value = false
  isModalVisible.value = true
}

const hideModal = () => {
  isModalVisible.value = false
  commentToDelete.value = null
}

const deleteComment = () => {
  if (commentToDelete.value !== null) {
    // props.comments = props.comments.filter((comment) => comment.id !== commentToDelete.value)
    hideModal()
  }
}
</script>
