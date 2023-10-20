<script setup lang="ts">
import { type ArticleDocument } from '@/client'
import UserItemSection from '@/components/users/UserItemSection.vue'
import { useUserStore } from '@/stores/UserStore'
import moment from 'moment'
import { computed, onBeforeMount, ref } from 'vue'
import { useRoute } from 'vue-router'

const props = defineProps<{
  article: ArticleDocument | undefined
}>()

const route = useRoute()

const formattedDate = ref<string>(moment(props.article?.created_at).format('Do MMMM YYYY'))
const isAllowedToEdit = ref<boolean>(false)

const editLink = computed(() => {
  return route.path + '/edit'
})

onBeforeMount(async () => {
  const currentUser = useUserStore().user
  if (currentUser?.role == 'Admin' || props.article?.author?.id == currentUser?._id) {
    isAllowedToEdit.value = true
  }
})
</script>

<template>
  <div class="row bg-secondary q-pa-md">
    <!-- Блок статьи -->
    <div class="col column shadow-2 q-pa-md">
      <!-- Header -->
      <div class="row justify-between items-center full-width">
        <!-- Аватар и имя автора -->
        <router-link
          :to="{ name: 'user', params: { id: article?.author?.id } }"
          class="row items-end text-h5 text-uppercase text-weight-bold text-white"
        >
          <UserItemSection :user="article?.author" small class="q-mr-md" />
          {{ article?.author?.username }}
        </router-link>
        <!-- Дата и теги -->
        <div class="col column items-end full-width">
          <div caption class="text-body flex-shrink">
            {{ formattedDate }}
          </div>
          <div v-if="article?.tags">
            <router-link
              v-for="tag in article?.tags"
              :key="tag"
              :to="{ name: 'home', query: { tag: tag } }"
            >
              <q-chip :label="tag" size="sm" dark color="primary" />
            </router-link>
          </div>
        </div>
      </div>

      <!-- Title статьи -->
      <q-item-label
        header
        lines="1"
        class="text-h5 text-white text-weight-bold text-center q-mb-md"
      >
        {{ article?.title }}
      </q-item-label>

      <!-- Текст статьи -->
      <q-item-label
        class="text-body1 text-white"
        v-html="article.content!.replace(/\n/g, '<br>')"
      />

      <!-- Кнопка "Редактировать статью" -->
      <q-btn
        v-if="isAllowedToEdit"
        label="Редактировать"
        :to="editLink"
        class="self-end text-body q-ma-md"
      />
    </div>
  </div>
</template>
