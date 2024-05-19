<script setup>
import { RouterLink, RouterView, useRoute } from 'vue-router'
const route = useRoute()
</script>

<template>
  <nav class="flex justify-between fixed w-screen items-center h-16 px-10 z-10">
    <RouterLink to="/">
      <h1 class="text-2xl font-extrabold text-primary-500">CINESPOT</h1>
    </RouterLink>
    <div class="flex gap-4">
      <RouterLink v-if="route.name !== 'signin' && route.name !== 'signup'" to="/signin">로그인</RouterLink>
      <RouterLink v-if="route.name !== 'signin' && route.name !== 'signup'" to="/mypage">마이페이지</RouterLink>
    </div>
  </nav>
  <div>
    <RouterView />
  </div>
</template>

<style scoped></style>
