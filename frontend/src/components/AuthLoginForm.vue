<script setup lang="ts">
import { ref } from 'vue'
import AuthService from '@/services/AuthService'

// reactive state
const username = ref('')
const password = ref('')

async function handleSubmit() {
  await AuthService.login(username.value, password.value)
}
</script>

<template>
  <q-card square class="shadow-24" style="width: 400px; height: 550px">
    <q-card-section class="bg-primary">
      <h4 class="text-white q-my-md">Войти в аккаунт</h4>
    </q-card-section>

    <q-form class="q-px-md q-pt-md" @submit.prevent="handleSubmit">
      <q-input
        v-model="username"
        label="Имя пользователя"
        clearable
        :input-style="{ fontSize: '25px' }"
      >
        <template v-slot:prepend><q-icon name="face" /></template>
      </q-input>
      <q-input
        v-model="password"
        type="password"
        label="Пароль"
        clearable
        :input-style="{ fontSize: '25px' }"
      >
        <template v-slot:prepend><q-icon name="lock" /></template>
      </q-input>

      <q-card-actions class="q-px-lg">
        <q-btn
          unelevated
          size="lg"
          color="secondary"
          type="submit"
          class="full-width text-white"
          label="Войти"
      /></q-card-actions>
    </q-form>
  </q-card>
</template>
