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
  <q-item class="row items-start bg-secondary q-pt-lg">
    <UserItemSection :user="article?.author" />

    <q-item-section class="col column items-start">
      <!-- Header статьи -->
      <div class="row justify-between items-center full-width">
        <q-btn
          v-if="isAllowedToEdit"
          label="Редактировать"
          :to="editLink"
          class="col-shrink text-body"
        />
        <div class="col column items-end full-width">
          <q-item-label caption class="text-body flex-shrink">
            {{ formattedDate }}
          </q-item-label>

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
      <q-item-label header lines="1" class="text-h5 self-center">
        {{ article?.title }}
      </q-item-label>

      <!-- Текст статьи -->
      <q-item-label
        class="text-body1 text-white"
        v-html="article.content!.replace(/\n/g, '<br>')"
      />
    </q-item-section>
  </q-item>
</template>
