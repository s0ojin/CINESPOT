<template>
  <div class="h-60 rounded-lg p-6 border hover:scale-105 transition duration-150 flex flex-col cursor-pointer">
    <div class="flex justify-between items-center">
      <h3 class="font-bold flex items-center gap-2">
        <img :src="review.userprofile" alt="Profile Image" class="w-6 h-6 rounded-full" />{{ review.user }}
      </h3>
      <div class="flex items-center">
        <span class="mr-2">{{ review.rating }}</span>
        <div class="flex">
          <i v-for="i in 5" :key="i" class="text-yellow-500">
            <i :class="i <= review.rating / 2 ? 'pi pi-star-fill' : 'pi pi-star'"></i>
          </i>
        </div>
      </div>
    </div>
    <p class="mb-auto mt-4">{{ truncatedContent }}</p>
    <div class="flex justify-end mt-2 items-center gap-4 text-slate-700">
      <div>
        <i class="pi pi-thumbs-up"></i>
        <span class="ml-2">{{ review.like_count }}</span>
      </div>
      <div>
        <i class="pi pi-comment"></i>
        <span class="ml-1">{{ review.comment_count }}</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, ref } from 'vue'

const props = defineProps({
  review: Object,
  contentLimit: {
    type: Number,
    default: 120
  }
})

const contentLimit = ref(props.contentLimit)

const truncatedContent = computed(() => {
  return props.review.content.length > contentLimit.value
    ? props.review.content.slice(0, contentLimit.value) + '...'
    : props.review.content
})
</script>
