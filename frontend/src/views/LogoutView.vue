<script setup lang="ts">
import AuthService from '@/services/AuthService'
import { onMounted } from 'vue'
import { useRouter } from 'vue-router';

onMounted(() => {
  AuthService.logout()
  useRouter().push("/")
})
</script>

<template>
  <q-page></q-page>
</template>
