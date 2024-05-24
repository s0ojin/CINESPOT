import { useQuery } from '@tanstack/vue-query'
import { getUserInfo } from '@/apis/authApi'

export const useAuthQuery = () => {
  return useQuery({
    queryKey: ['auth'],
    queryFn: async () => {
      const token = localStorage.getItem('token')
      if (token) {
        const userInfo = await getUserInfo()
        return { token, userInfo: userInfo.data }
      }
      throw new Error('token이 존재하지 않습니다.')
    },
    staleTime: Infinity,
    cacheTime: Infinity,
    refetchOnWindowFocus: false
  })
}
