<script setup lang="ts">
import { type ArticleDocument } from '@/client'
import UserItemSection from '@/components/users/UserItemSection.vue'

const props = defineProps<{
  article: ArticleDocument | undefined
}>()
</script>

<template>
  <q-item class="row items-start bg-secondary">
    <UserItemSection />

    <q-item-section class="col column items-start">
      <q-item-label header lines="1" class="text-h5">
        {{ article?.title }}
      </q-item-label>
      <q-item-label caption class="text-body">{{ article?.created_at }}</q-item-label>
      <q-item-label class="text-body1 text-white">{{ article?.content }}</q-item-label>
    </q-item-section>
  </q-item>
</template>
