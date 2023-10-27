<script setup lang="ts">
import { type UserDocument } from '@/client'

const props = defineProps<{ currentUser?: UserDocument }>()
</script>

<template>
  <q-toolbar>
    <q-toolbar-title>
      <q-avatar>
        <img src="https://img.icons8.com/3d-fluency/94/disguised-face-1.png" />
      </q-avatar>
      <q-btn :to="{ name: 'home' }" stretch flat>fastapi-mongodb-vue-blog</q-btn>
      <router-link to="{ name: 'about' }" custom>by Desunovu</router-link>
    </q-toolbar-title>

    <q-space />

    <div v-if="!currentUser" class="row">
      <q-btn :to="{ name: 'login' }" stretch flat label="Войти" />
      <q-btn :to="{ name: 'register' }" stretch flat label="Зарегестрироваться" />
    </div>
    <div v-else class="row">
      <!-- Блок который показывается если пользователь администратор или автор -->
      <div v-if="currentUser.role == 'Admin' || currentUser.role == 'Author'" class="text-accent">
        <q-btn :to="{ name: 'create-article' }" label="Написать статью" flat />
      </div>
      <!-- Блок который показывается если пользователь администратор -->
      <div v-if="currentUser.role == 'Admin'" class="text-accent">
        <q-btn :to="{ name: 'gpt-writer' }" label="GptWriter" flat />
      </div>
      <!-- Блок для всех пользователей -->
      <q-btn :to="{ name: 'home' }" stretch flat label="Все статьи" />
      <q-btn :to="{name: 'users'}" stretch flat label="Пользователи" />
      <q-btn :to="{ name: 'profile' }" stretch flat>{{ currentUser.username }}</q-btn>
      <q-btn :to="{ name: 'logout' }" stretch flat label="Выйти" />
    </div>
  </q-toolbar>
</template>
