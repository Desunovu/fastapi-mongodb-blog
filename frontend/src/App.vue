<script setup lang="ts">
import { RouterView } from 'vue-router'
import NavbarMenu from './components/NavbarMenu.vue';
import { useUserStore } from './stores/UserStore';


const userStore = useUserStore()
</script>

<template>
  <q-layout view="lHh Lpr lFf" class="WAL bg-image">
    <q-header reveal elevated>
      <NavbarMenu :currentUser="userStore.user" />
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
