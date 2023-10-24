import { createRouter, createWebHistory } from 'vue-router'
import AuthLoginView from '@/views/AuthLoginView.vue'
import AuthRegisterView from '@/views/AuthRegisterView.vue'
import ArticleListView from '@/views/ArticleListView.vue'
import AuthLogoutView from '@/views/AuthLogoutView.vue'
import ArticleCardView from '@/views/ArticleCardView.vue'
import UserView from '@/views/UserView.vue'
import ArticleEditorView from '@/views/ArticleEditorView.vue'
import PathNotFoundView from '@/views/PathNotFoundView.vue'
import GptWriterView from '@/views/GptWriterView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    // LOGIN AND REGISTER
    { path: '/login', name: 'login', component: AuthLoginView },
    { path: '/register', name: 'register', component: AuthRegisterView },
    { path: '/logout', name: 'logout', component: AuthLogoutView },
    // ARTICLES
    { path: '/', name: 'home', component: ArticleListView },
    { path: '/create-article', name: 'create-article', component: ArticleEditorView },
    { path: '/article/:id', name: 'article', component: ArticleCardView },
    { path: '/article/:id/edit', name: 'edit-article', component: ArticleEditorView },
    //GPT-WRITER
    { path: '/gpt-writer', name: 'gpt-writer', component: GptWriterView },
    // USERS
    { path: '/user/:id', name: 'user', component: UserView },
    { path: '/profile', name: 'profile', component: UserView },
    // NOT FOUND
    { path: '/:pathMatch(.*)*', component: PathNotFoundView }
  ]
})

export default router
