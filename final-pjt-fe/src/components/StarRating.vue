<template>
  <div class="flex cursor-pointer" @mouseleave="resetHoverRating">
    <div v-for="star in 5" :key="star" class="relative inline-block w-12 h-12">
      <div
        class="absolute w-6 h-12 left-0 transition-colors duration-300"
        @mousemove="setHoverRating(star - 0.5)"
        @click="setRating(star - 0.5)"
      >
        <svg viewBox="0 0 12 24" class="w-full h-full fill-current" :class="getStarClass(star - 0.5)">
          <defs>
            <clipPath :id="'half-star-left-' + star">
              <rect x="0" y="0" width="12" height="24" />
            </clipPath>
          </defs>
          <polygon
            points="12,2 15,8 22,9 17,14 18,21 12,18 6,21 7,14 2,9 9,8"
            :clip-path="'url(#half-star-left-' + star + ')'"
          />
        </svg>
      </div>

      <div
        class="absolute w-6 h-12 left-6 transition-colors duration-300"
        @mousemove="setHoverRating(star)"
        @click="setRating(star)"
      >
        <svg viewBox="12 0 12 24" class="w-full h-full fill-current" :class="getStarClass(star)">
          <defs>
            <clipPath :id="'half-star-right-' + star">
              <rect x="12" y="0" width="12" height="24" />
            </clipPath>
          </defs>
          <polygon
            points="12,2 15,8 22,9 17,14 18,21 12,18 6,21 7,14 2,9 9,8"
            :clip-path="'url(#half-star-right-' + star + ')'"
          />
        </svg>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const rating = ref(0)
const hoverRating = ref(0)

const resetHoverRating = () => {
  hoverRating.value = 0
}

const setHoverRating = (value) => {
  hoverRating.value = value
}

const setRating = (value) => {
  rating.value = value
}

const getStarClass = (value) => {
  const totalRating = hoverRating.value || rating.value
  return totalRating >= value ? 'text-yellow-400' : 'text-gray-200'
}
</script>
