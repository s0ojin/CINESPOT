<template>
  <div class="max-w-sm rounded-lg overflow-hidden shadow-lg my-4">
    <img :src="image_url" alt="Destination image" class="w-full" />
    <div class="px-6 py-4">
      <div class="font-bold text-xl mb-2">{{ destination }}</div>
      <p class="text-gray-700 text-base">
        {{ reason }}
      </p>
    </div>
    <div class="px-6 pt-4 pb-2">
      <span class="inline-block bg-gray-200 rounded-full px-3 py-1 text-sm font-semibold text-gray-700 mr-2 mb-2">{{
        address
      }}</span>
    </div>
  </div>
</template>

<script setup>
defineProps({
  destination: String,
  reason: String,
  address: String,
  image_url: String
})
</script>
