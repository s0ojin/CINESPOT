import { createRouter, createWebHistory } from 'vue-router'
import MovieListView from '@/views/MovieListView.vue'
import MovieDetailView from '@/views/MovieDetailView.vue'
import SignUpView from '@/views/SignUpView.vue'
import SignInView from '@/views/SignInView.vue'
import MypageView from '@/views/MypageView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/movies',
      name: 'movies',
      component: MovieListView
    },
    {
      path: '/movies/:movieId',
      name: 'movieDetail',
      component: MovieDetailView
    },
    {
      path: '/signup',
      name: 'signup',
      component: SignUpView
    },
    {
      path: '/signin',
      name: 'signin',
      component: SignInView
    },
    {
      path: '/mypage',
      name: 'mypage',
      component: MypageView
    }
  ]
})

export default router
