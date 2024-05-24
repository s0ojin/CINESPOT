<template>
  <div class="max-w-sm rounded-lg overflow-hidden shadow-lg my-4 flex flex-col">
    <img :src="travel.image_url" alt="Destination image" class="w-full h-48 object-cover" />
    <div class="px-6 py-4">
      <div class="font-bold text-xl mb-2">{{ travel.destination }}</div>
      <p class="text-gray-700 text-base h-auto">
        {{ travel.reason }}
      </p>
    </div>
    <div class="px-6 pt-4 pb-2 mt-auto">
      <span class="inline-block bg-gray-200 rounded-full px-3 py-1 text-sm font-semibold text-gray-700 mr-2 mb-2">{{
        travel.address
      }}</span>
    </div>
  </div>
</template>

<script setup>
defineProps({
  travel: Object
})
</script>
