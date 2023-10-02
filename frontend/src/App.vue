<script setup lang="ts">
import { RouterLink, RouterView } from 'vue-router'
import { useUserStore } from './stores/UserStore'
import { OpenAPI } from './client'

const userStore = useUserStore()
</script>

<template>
  <q-layout view="lHh Lpr lFf" class="WAL bg-image">
    <q-header reveal elevated>
      <q-toolbar>
        <q-toolbar-title>
          <q-avatar>
            <img src="https://img.icons8.com/3d-fluency/94/disguised-face-1.png" />
          </q-avatar>
          <q-btn to="/" stretch flat>fastapi-mongodb-vue-blog</q-btn>
          <router-link to="/about" custom>by Desunovu</router-link>
        </q-toolbar-title>

        <q-space />

        <div v-if="!userStore.user">
          <q-btn to="/login" stretch flat label="Войти" />
          <q-btn to="/register" stretch flat label="Зарегестрироваться" />
        </div>
        <div v-else>
          <q-btn to="/create-article" label="Написать статью" flat class="text-info"/>
          <q-btn to="/" stretch flat label="Все статьи" />
          <q-btn to="/profile" stretch flat>{{ userStore.user?.username }}</q-btn>
          <q-btn to="/logout" stretch flat label="Выйти" />
        </div>
      </q-toolbar>
    </q-header>

    <q-page-container class="window-hight row justify-center">
      <div style="min-width: 700px; max-width: 700px">
        <RouterView />
      </div>
    </q-page-container>
  </q-layout>
</template>

<style>
.bg-image {
  background-image: url(https://img.freepik.com/free-vector/black-triangles-pattern_1060-57.jpg);
  background-repeat: repeat;
  background-size: contain;
}
.WAL {
  width: 100%;
  height: 100%;
  padding-top: 20px;
  padding-bottom: 20px;
}
</style>
