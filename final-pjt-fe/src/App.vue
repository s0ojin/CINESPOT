<script setup>
import { RouterLink, RouterView } from 'vue-router'
</script>

<template>
  <header>
    <nav class="flex justify-between h-16 bg-slate-50">
      <RouterLink to="/movies">LOGO</RouterLink>
      <div class="flex gap-4">
        <RouterLink to="/signup">SignUp</RouterLink>
        <RouterLink to="/signin">SignIn</RouterLink>
        <RouterLink to="/mypage">Mypage</RouterLink>
      </div>
    </nav>
  </header>
  <RouterView />
</template>

<style scoped></style>
