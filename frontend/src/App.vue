<script setup lang="ts">
import { RouterLink, RouterView } from 'vue-router'
import { useUserStore } from './stores/UserStore'
import { OpenAPI } from './client'

const userStore = useUserStore()
</script>

<template>
  <q-layout view="hHh lpR fFf">
    <q-header reveal elevated class="bg-primary text-white">
      <q-toolbar>
        <q-toolbar-title>
          <q-avatar>
            <img src="https://img.icons8.com/3d-fluency/94/disguised-face-1.png" />
          </q-avatar>
          fastapi-mongodb-vue-blog by Desunovu
        </q-toolbar-title>

        <q-space />

        <q-btn to="/" stretch flat label="Все статьи" />
        <template v-if="!userStore.user">
          <q-btn to="/login" stretch flat label="Войти" />
          <q-btn to="/register" stretch flat label="Зарегестрироваться" />
        </template>
        <template v-else>
          <q-btn to="/profile" stretch flat>{{ userStore.user?.username }}</q-btn>
          <q-btn to="/logout" stretch flat label="Выйти" />
        </template>
      </q-toolbar>
    </q-header>

    <q-page-container
      class="window-height window-width row justify-center items-center"
      style="background: linear-gradient(#4c4c4c, #191919)"
    >
      <RouterView />
    </q-page-container>
  </q-layout>
</template>

<style></style>
