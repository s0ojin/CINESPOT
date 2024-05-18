<template>
  <div class="flex h-screen justify-center items-center">
    <div class="absolute inset-0 bg-gradient-to-t from-transparent via-white/50 to-white"></div>
    <img
      src="https://source.unsplash.com/random?nature&q=full"
      alt="Signup Background"
      class="w-full h-full object-cover"
    />
    <div class="absolute w-1/3 p-20 pb-14 bg-white rounded-2xl shadow-2xl flex flex-col justify-center gap-12">
      <form class="flex flex-col gap-6 w-full">
        <div class="mb-8 flex flex-col gap-2 items-center">
          <h2 class="text-4xl font-bold text-primary-500">환영합니다</h2>
          <p class="text-primary-900">이메일로 간편하게 가입해보세요!</p>
        </div>
        <div class="relative">
          <input type="text" class="input peer" v-model="email" placeholder="" />
          <label class="input-label">EMAIL</label>
        </div>
        <div class="relative">
          <input type="password" class="input peer" v-model="password" placeholder="" />
          <label class="input-label">PASSWORD</label>
        </div>
        <div class="relative">
          <input type="password" class="input peer" v-model="passwordConfirm" placeholder="" />
          <label class="input-label">PASSWORD CONFIRM</label>
        </div>
        <button class="submit-btn">회원가입</button>
      </form>
      <p class="text-slate-500 mx-auto text-sm">
        이미 회원이신가요?
        <RouterLink to="/signin" class="text-slate-600 text-base font-medium ml-1">로그인</RouterLink>
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { RouterLink } from 'vue-router'

const email = ref('')
const password = ref('')
const passwordConfirm = ref('')
</script>
