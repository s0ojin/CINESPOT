<template>
  <div v-if="!isLoading && mypageInfo" class="flex justify-center">
    <h1 class="text-lg">안녕하세요 {{ mypageInfo.username }}님!</h1>
  </div>
</template>

<script setup>
import { useQuery } from '@tanstack/vue-query'
import { getMypageInfo } from '@/apis/authApi'

const { data: mypageInfo, isLoading } = useQuery({
  queryKey: ['mypage'],
  queryFn: () => getMypageInfo().then((res) => res.data)
})
</script>
