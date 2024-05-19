<script setup>
import { computed } from 'vue'
import { RouterLink, RouterView, useRoute } from 'vue-router'
const route = useRoute()

const containerClass = computed(() => {
  return route.meta.noContainer ? '' : 'max-w-screen-xl mx-auto pt-16'
})
</script>

<template>
  <nav class="w-full fixed z-10">
    <div class="h-16 max-w-screen-xl mx-auto flex justify-between items-center">
      <RouterLink to="/">
        <h1 class="text-2xl font-extrabold text-primary-500">CINESPOT</h1>
      </RouterLink>
      <div class="flex gap-4">
        <RouterLink v-if="route.name !== 'signin' && route.name !== 'signup'" to="/signin">로그인</RouterLink>
        <RouterLink v-if="route.name !== 'signin' && route.name !== 'signup'" to="/mypage">마이페이지</RouterLink>
      </div>
    </div>
  </nav>
  <div :class="containerClass">
    <RouterView />
  </div>
</template>

<style scoped></style>
