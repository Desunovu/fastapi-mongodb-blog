<script setup lang="ts">
import { computed, onBeforeMount, ref } from 'vue'
import UserInfoCard from './UserInfoCard.vue'
import { DefaultService, UsersSortField, type UserDocument, SortDirection } from '@/client'
import { useUserStore } from '@/stores/UserStore'
import { Notify } from 'quasar'

const users = ref<UserDocument[]>([])
const limit = ref<number>(10)
const skip = ref<number>(0)
const sortBy = ref<UsersSortField>(UsersSortField.CREATED_AT)
const sortOrder = ref<SortDirection>(SortDirection._1)

const currentUserIsAdmin = computed(() => {
  return useUserStore().user?.role === 'Admin'
})

// Функция для загрузки дополнительных пользователей
const loadMoreUsers = async () => {
  console.debug('Загрузка пользователей')
  const usersResponse = await DefaultService.listUsersUsersGet(
    skip.value,
    limit.value,
    sortBy.value,
    sortOrder.value
  )
  users.value.push(...usersResponse.users)
  skip.value += limit.value
  return usersResponse.users.length
}

// Функция для загрузки при прокрутке
const loadMore = async (_index: number, done: CallableFunction) => {
  const usersLoaded = await loadMoreUsers()
  done(usersLoaded > 0 ? false : true)
}

// Функция сброса при смене параметров сортировки
const handleSelectorChange = async () => {
  users.value = []
  skip.value = 0
  limit.value = 10
  await loadMoreUsers()
}

const handleDisableUserButton = async (userId: string) => {
  await DefaultService.disableUserUsersUserIdDisablePut(userId)
  Notify.create('Пользователь ' + userId + ' отключен')
}

onBeforeMount(async () => {
  await loadMoreUsers()
})
</script>

<template>
  <div class="column bg-secondary q-pa-md">
    <!-- Header -->
    <div class="row justify-end q-mb-md">
      <!-- Селекторы сортировки  -->
      <q-select
        v-model="sortBy"
        :options="[
          { label: 'По дате создания', value: UsersSortField.CREATED_AT },
          { label: 'По имени пользователя', value: UsersSortField.USERNAME }
        ]"
        emit-value
        map-options
        label="Сортировать по"
        @update:model-value="handleSelectorChange"
        class="col-3"
      />
      <q-select
        v-model="sortOrder"
        :options="[
          { label: 'По возрастанию', value: SortDirection['_1'] },
          { label: 'По убыванию', value: SortDirection['_-1'] }
        ]"
        emit-value
        map-options
        label="Порядок"
        @update:model-value="handleSelectorChange"
        class="col-3 q-ml-md"
      />
    </div>

    <!-- Список пользователей -->
    <q-list separator padding>
      <!-- Бесконечная прокрутка -->
      <q-infinite-scroll @load="loadMore" :offset="10">
        <!-- Пользователь -->
        <div v-for="user in users" :key="user._id!" class="row shadow-2 q-mb-lg q-pa-sm">
          <!-- Аватар и имя автора -->
          <router-link :to="{ name: 'user', params: { id: user._id } }" class="user-link col-2">
            <UserInfoCard :user="user" />
          </router-link>
          <!-- Информация о пользователе -->
          <div class="col-grow q-mx-md">
            <div class="row items-center">
              <div class="text-h6">{{ user.username }}</div>
              <div class="text-subtitle2 q-ml-sm">
                ({{ user.role ?? 'Аккаунт не подтвержден' }})
              </div>
              <div v-if="user.disabled" class="text-subtitle2 q-ml-sm text-negative">
                [Заблокирован]
              </div>
            </div>
            <div class="text-subtitle2">{{ user.email }}</div>
            <div class="text-subtitle2">Комментариев: {{ user.comments_count ?? 'NULL' }}</div>
          </div>
          <!-- Действия -->
          <div v-if="currentUserIsAdmin" class="col-2">
            <div class="text-center">Действия администратора</div>
            <q-separator class="q-mb-sm" />
            <q-btn
              v-if="!user.disabled"
              class="q-mb-sm"
              label="Заблокировать"
              @click="handleDisableUserButton(user._id!)"
              flat
            />
          </div>
        </div>
      </q-infinite-scroll>
    </q-list>
  </div>
</template>

<style scoped>
.user-link {
  text-decoration: none;
}
</style>
