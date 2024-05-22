<template>
  <div class="border p-6 rounded-lg">
    <h1 class="text-xl mb-1">박경령차영차님 이 작품에 대해 어떻게 생각하세요?</h1>
    <StarRating />
    <textarea
      name=""
      id=""
      class="input resize-none h-28 pt-2 mt-2"
      placeholder="영화에 대한 감상평이나 기대평을 남겨주세요!"
    ></textarea>
    <button class="submit-btn w-full h-10 rounded-lg">리뷰 남기기</button>
  </div>
</template>

<script setup>
import StarRating from '@/components/StarRating.vue'
</script>
