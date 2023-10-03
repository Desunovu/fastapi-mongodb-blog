<script setup lang="ts">
import { type ArticleDocument } from '@/client'
import UserItemSection from '@/components/users/UserItemSection.vue'
import { useUserStore } from '@/stores/UserStore'
import moment from 'moment'
import { computed, onMounted, ref } from 'vue'
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

onMounted(() => {
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
      <q-item-label caption class="text-body self-end">
        {{ formattedDate }}
      </q-item-label>

      <q-btn v-if="isAllowedToEdit" label="Редактировать" :to="editLink" class="text-body self-end" />

      <q-item-label header lines="1" class="text-h5 self-center">
        {{ article?.title }}
      </q-item-label>

      <q-item-label class="text-body1 text-white">
        {{ article?.content }}
      </q-item-label>
    </q-item-section>
  </q-item>
</template>
