<template>
  <RouterLink :to="{ name: 'reviewDetail', params: { reviewId: review.id } }">
    <div class="h-60 rounded-lg p-6 border hover:scale-105 transition duration-150 flex flex-col">
      <div class="flex justify-between items-center">
        <h3 class="font-bold flex items-center gap-2">
          <img :src="review.userprofile" alt="Profile Image" class="w-6 h-6 rounded-full" />{{ review.user }}
        </h3>
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
  </RouterLink>
</template>

<script setup>
import { computed, ref } from 'vue'
import { getStarStatus } from '@/utils/getStarStatus'

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
