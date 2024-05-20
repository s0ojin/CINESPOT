<template>
  <div class="h-60 rounded-lg p-6 border hover:scale-105 transition duration-150 flex flex-col">
    <div class="flex justify-between items-center">
      <h3 class="font-bold flex items-center gap-2">
        <img :src="review.authorProfile" alt="Profile Image" class="w-6 h-6 rounded-full" />{{ review.author }}
      </h3>
      <div class="flex items-center">
        <span class="mr-2">{{ review.score }}</span>
        <div class="flex">
          <i v-for="i in 5" :key="i" class="text-yellow-500">
            <i :class="i <= review.score / 2 ? 'pi pi-star-fill' : 'pi pi-star'"></i>
          </i>
        </div>
      </div>
    </div>
    <p class="mb-auto mt-4">{{ truncatedContent }}</p>
    <div class="flex justify-end mt-2 items-center gap-4">
      <button @click="toggleLike" :class="{ 'text-red-500': liked }">
        <i :class="[liked ? 'pi pi-thumbs-up-fill' : 'pi pi-thumbs-up']"></i>
        <span class="ml-2">{{ likeCount }}</span>
      </button>
      <div>
        <i class="pi pi-comment"></i>
        <span class="ml-1">{{ review.comments.length }}</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, ref } from 'vue'

const props = defineProps({
  review: Object
})

const liked = ref(false)
const likeCount = ref(props.review.likes)

const toggleLike = () => {
  liked.value = !liked.value
  likeCount.value += liked.value ? 1 : -1
}

const truncatedContent = computed(() => {
  return props.review.content.length > 120 ? props.review.content.slice(0, 120) + '...' : props.review.content
})
</script>
