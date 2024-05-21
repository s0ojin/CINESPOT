import { useQuery } from '@tanstack/vue-query'

export const useAuthQuery = () => {
  return useQuery({
    queryKey: ['auth'],
    queryFn: async () => {
      const token = localStorage.getItem('token')
      if (token) {
        return { token }
      }
      throw new Error('token이 존재하지 않습니다.')
    },
    staleTime: Infinity,
    cacheTime: Infinity,
    refetchOnWindowFocus: false
  })
}
