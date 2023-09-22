import { createRouter, createWebHistory } from 'vue-router'
import LoginView from '@/views/LoginView.vue'
import HomeView from '@/views/HomeView.vue'
import LogoutView from '@/views/LogoutView.vue'
import ArticleView from '@/views/ArticleView.vue'
import UserView from '@/views/UserView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/login',
      name: 'login',
      component: LoginView
    },
    {
      path: '/logout',
      name: 'logout',
      component: LogoutView
    },
    {
      path: '/article/:id',
      name: 'article',
      component: ArticleView
    },
    {
      path: '/user/:id',
      name: 'user',
      component: UserView
    },
    {
      path: '/profile',
      name: 'profile',
      component: UserView
    }
  ]
})

export default router
