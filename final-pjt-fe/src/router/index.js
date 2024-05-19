import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '@/views/HomeView.vue'
import MovieDetailView from '@/views/MovieDetailView.vue'
import SignUpView from '@/views/SignUpView.vue'
import SignInView from '@/views/SignInView.vue'
import MypageView from '@/views/MypageView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/movies/:movieId',
      name: 'movieDetail',
      component: MovieDetailView
    },
    {
      path: '/signup',
      name: 'signup',
      component: SignUpView,
      meta: { noContainer: true }
    },
    {
      path: '/signin',
      name: 'signin',
      component: SignInView,
      meta: { noContainer: true }
    },
    {
      path: '/mypage',
      name: 'mypage',
      component: MypageView
    }
  ]
})

export default router
