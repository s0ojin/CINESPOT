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
  <div v-if="!route.meta.noContainer || route.name === 'movieDetail'">
    <footer class="h-72 bg-gray-100 pt-10 pb-14 text-slate-500 mt-40 text-sm">
      <div class="h-full max-w-screen-xl mx-auto flex flex-col">
        <div class="flex justify-between h-full">
          <address class="not-italic flex flex-col gap-1">
            <h1 class="text-2xl font-extrabold mb-1 hover:text-primary-500"><a href="#">CINESPOT</a></h1>
            <p class="text-base mb-4">서비스이용약관없음주의 | 개인정보수집동의는받지않았지만잘처리하겠음</p>
            <p>
              대외협력 | <a href="https://www.ssafy.com/" class="hover:text-slate-800">삼성 청년 SW 아카데미 11th</a>
            </p>
            <p class="mb-4">박수진챠진짜박경령차영차 | 서울 강남구 테헤란로 212 멀티캠퍼스 역삼 201호</p>
            <p class="mt-auto">Copyright © 2024 ssafy-11th. All rights reserved.</p>
          </address>
          <div class="flex items-center text-2xl gap-4 mt-auto">
            <a href="mailto:onepst@hanyang.ac.kr">
              <svg
                xmlns="http://www.w3.org/2000/svg"
                viewBox="0 0 512 512"
                fill="current"
                width="current"
                class="h-6 fill-slate-500 hover:fill-slate-800"
              >
                <path
                  d="M48 64C21.5 64 0 85.5 0 112c0 15.1 7.1 29.3 19.2 38.4L236.8 313.6c11.4 8.5 27 8.5 38.4 0L492.8 150.4c12.1-9.1 19.2-23.3 19.2-38.4c0-26.5-21.5-48-48-48H48zM0 176V384c0 35.3 28.7 64 64 64H448c35.3 0 64-28.7 64-64V176L294.4 339.2c-22.8 17.1-54 17.1-76.8 0L0 176z"
                />
              </svg>
            </a>
            <a href="https://lab.ssafy.com/one_pst/10-pjt" class="hover:text-slate-800">
              <i class="pi pi-github"></i>
            </a>
          </div>
        </div>
      </div>
    </footer>
  </div>
</template>

<style scoped></style>
