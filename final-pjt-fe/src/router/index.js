import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '@/views/HomeView.vue'
import MovieDetailView from '@/views/MovieDetailView.vue'
import SignUpView from '@/views/SignUpView.vue'
import SignInView from '@/views/SignInView.vue'
import MypageView from '@/views/MypageView.vue'
import ReviewDetailView from '@/views/ReviewDetailView.vue'
import ReviewListView from '@/views/ReviewListView.vue'
import ReviewUpdateView from '@/views/ReviewUpdateView.vue'

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
      component: MovieDetailView,
      meta: { noContainer: true }
    },
    {
      path: '/movies/:movieId/reviews',
      name: 'movieReviewList',
      component: ReviewListView
    },
    {
      path: '/signup',
      name: 'signup',
      component: SignUpView,
      meta: { noContainer: true, logoutRequired: true }
    },
    {
      path: '/signin',
      name: 'signin',
      component: SignInView,
      meta: { noContainer: true, logoutRequired: true }
    },
    {
      path: '/reviews/:reviewId',
      name: 'reviewDetail',
      component: ReviewDetailView
    },
    {
      path: '/reviews/:reviewId/edit',
      name: 'reviewUpdate',
      component: ReviewUpdateView,
      meta: { authRequired: true }
    },
    {
      path: '/mypage',
      name: 'mypage',
      component: MypageView,
      meta: { authRequired: true }
    }
  ]
})

router.beforeEach((to, from, next) => {
  const isLoggedIn = localStorage.getItem('token')

  if (to.meta.authRequired && !isLoggedIn) {
    next({ name: 'signin' })
  } else if (to.meta.logoutRequired && isLoggedIn) {
    next({ name: 'home' })
  } else {
    next()
  }
})

export default router
