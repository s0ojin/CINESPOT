<template>
  <div class="flex h-screen justify-center items-center">
    <div class="absolute inset-0 bg-gradient-to-t from-transparent via-white/50 to-white"></div>
    <img
      src="https://source.unsplash.com/random?nature&q=full"
      alt="Signin Background"
      class="w-full h-full object-cover"
    />
    <div class="absolute w-1/3 p-20 pb-14 bg-white rounded-2xl shadow-2xl flex flex-col justify-center gap-12">
      <form @submit.prevent="handleSignIn" class="flex flex-col gap-6 w-full">
        <div class="mb-8 flex flex-col gap-2 items-center">
          <h2 class="text-4xl font-bold text-primary-500">CINESPOT</h2>
          <p class="text-primary-900">영화 속 그 장소, CINESPOT에서 찾아줄게요!</p>
        </div>
        <div class="relative">
          <input type="text" class="input peer" v-model="username" placeholder="" />
          <label class="input-label">USERNAME</label>
        </div>
        <div class="relative">
          <input type="password" class="input peer" v-model="password" placeholder="" />
          <label class="input-label">PASSWORD</label>
        </div>
        <button class="submit-btn">로그인</button>
      </form>
      <p class="text-slate-500 mx-auto text-sm">
        아직 회원이 아니신가요?
        <RouterLink to="/signup" class="text-slate-600 text-base font-medium ml-1">회원가입</RouterLink>
      </p>
    </div>
  </div>
</template>

<script setup>
import { getUserInfo, postSignIn } from '@/apis/authApi'
import { useMutation, useQueryClient } from '@tanstack/vue-query'
import { ref } from 'vue'
import { RouterLink, useRouter } from 'vue-router'

const username = ref('')
const password = ref('')
const router = useRouter()
const queryClient = useQueryClient()

const signInMutation = useMutation({
  mutationFn: postSignIn,
  onSuccess: async (data) => {
    const token = data.data.key
    localStorage.setItem('token', token)

    try {
      const userInfoResponse = await getUserInfo()
      const userInfo = userInfoResponse.data
      queryClient.setQueryData(['auth'], { token, userInfo })
    } catch (err) {
      console.error('유저정보 가져오기에 실패했습니다.', err)
    }

    alert('로그인 성공!')
    router.push('/')
  },
  onError: (err) => {
    alert('로그인 실패!', err)
  }
})

const handleSignIn = () => {
  signInMutation.mutate({ username: username.value, password: password.value })
}
</script>
