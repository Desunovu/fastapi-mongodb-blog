<script setup lang="ts">
import { DefaultService, type UserDocument } from '@/client'
import UserCard from '@/components/users/UserCard.vue'
import AuthService from '@/services/AuthService'
import { useUserStore } from '@/stores/UserStore'
import { onMounted, ref } from 'vue'
import { useRoute } from 'vue-router'

const user = ref<UserDocument>()
const editable = ref<boolean>(false)
const isProfile = ref<boolean>(false)

const route = useRoute()

onMounted(async () => {
  const current_user = useUserStore().user

  if (route.path == '/profile') {
    AuthService.update_user_info()
    user.value = current_user
    isProfile.value = true
    // разрешить редактировать свою страницу
    editable.value = true
  } else {
    const userId = route.params.id.toString()
    if (userId == current_user?._id) {isProfile.value = true}
    const userResponse = await DefaultService.getUserByIdUsersUserIdGet(userId)
    user.value = userResponse.user
    // разрешить администратору редактировать страницы
    editable.value = current_user?.role == 'Admin' ? true : false
  }
})
</script>

<template>
  <q-page padding>
    <UserCard :isProfile="isProfile" :editable="editable" :user="user" />
  </q-page>
</template>
