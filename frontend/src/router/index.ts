import { createRouter, createWebHistory } from 'vue-router'
import LoginView from '@/views/LoginView.vue'
import HomeView from '@/views/HomeView.vue'
import LogoutView from '@/views/LogoutView.vue'
import ArticleView from '@/views/ArticleView.vue'
import UserView from '@/views/UserView.vue'
import EditArticleView from '@/views/EditArticleView.vue'
import PathNotFound from '@/views/PathNotFound.vue'
import GptWriterView from '@/views/GptWriterView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: '/', name: 'home', component: HomeView },
    { path: '/login', name: 'login', component: LoginView },
    { path: '/logout', name: 'logout', component: LogoutView },
    { path: '/create-article', name: 'create-article', component: EditArticleView },
    { path: '/article/:id', name: 'article', component: ArticleView },
    { path: '/article/:id/edit', name: 'edit-article', component: EditArticleView },
    { path: '/user/:id', name: 'user', component: UserView },
    { path: '/profile', name: 'profile', component: UserView },
    //GPT-WRITER
    { path: '/gpt-writer', name: 'gpt-writer', component: GptWriterView },
    { path: '/:pathMatch(.*)*', component: PathNotFound }
  ]
})

export default router
