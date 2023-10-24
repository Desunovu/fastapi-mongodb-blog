<script setup lang="ts">
import { RouterView } from 'vue-router'
import HeaderMenu from './components/HeaderMenu.vue'
import { useUserStore } from './stores/UserStore'

const userStore = useUserStore()
</script>

<template>
  <q-layout view="lHh Lpr lFf" class="WAL background-image">
    <q-header reveal elevated>
      <HeaderMenu :currentUser="userStore.user" />
    </q-header>

    <q-page-container class="column items-center">
      <div class="content-width">
        <RouterView />
      </div>
    </q-page-container>
  </q-layout>
</template>

<style>
.background-image {
  background-image: linear-gradient(rgba(0, 0, 0, 0.8), rgba(0, 0, 0, 0.8)),
    url(https://img.freepik.com/free-vector/black-triangles-pattern_1060-57.jpg);
  background-repeat: repeat;
  background-size: 700px;
  background-color: rgba(0, 0, 0, 0.9);
}

.WAL {
  padding-top: 20px;
  padding-bottom: 20px;
}

/* Ограниение по ширине для всего контента сайта в процентах */
.content-width {
  min-width: 70%;
  max-width: 70%;
}
</style>
