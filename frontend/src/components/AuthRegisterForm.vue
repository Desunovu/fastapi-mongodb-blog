<script setup lang="ts">
import { DefaultService } from '@/client'
import AuthService from '@/services/AuthService'
import { Notify } from 'quasar'
import { ref } from 'vue'

const username = ref('')
const email = ref('')
const password = ref('')
const confirmPassword = ref('')

const handleSubmit = async () => {
  // Проверка совпадения паролей
  if (password.value != confirmPassword.value) {
    Notify.create('Пароли не совпадают')
    return
  }

  const registerResponse = await DefaultService.registerUserRegisterPost({
    username: username.value,
    password: password.value,
    email: email.value
  })

  Notify.create('Регистрация прошла успешно. Создан аккаунт: ' + registerResponse.username)

  await AuthService.login(username.value, password.value)
}
</script>

<template>
  <div>
    <q-card square class="shadow-24" style="width: 400px; height: 550px">
      <q-card-section class="bg-primary">
        <h4 class="text-white q-my-md">Регистрация</h4>
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

        <q-input v-model="email" label="E-mail" clearable :input-style="{ fontSize: '25px' }">
          <template v-slot:prepend><q-icon name="mail" /></template>
        </q-input>

        <q-input
          v-model="password"
          type="password"
          label="Пароль"
          F
          clearable
          :input-style="{ fontSize: '25px' }"
        >
          <template v-slot:prepend><q-icon name="lock" /></template>
        </q-input>

        <q-input
          v-model="confirmPassword"
          type="password"
          label="Подтвердите пароль"
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
            label="Зарегистрироваться"
        /></q-card-actions>
      </q-form>
    </q-card>
  </div>
</template>
