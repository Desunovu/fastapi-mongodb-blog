<script setup lang="ts">
import { DefaultService, type ArticleDocument } from '@/client'
import { onMounted, ref } from 'vue'

const props = defineProps({
  articles: Array<ArticleDocument>
})

</script>

<template>
  <q-list separator>
    <q-item v-for="article in articles" :key="article._id ?? ''">
      <q-item-section top avatar style="width: 15%;">
        <q-avatar rounded>
          <img src="https://cdn.quasar.dev/img/boy-avatar.png" />
        </q-avatar>
        <q-item-label class="text-body ellipsis text-white">Густаво 1111111111111111111111111111111111111111111111111111111111111</q-item-label>
      </q-item-section>

      <q-item-section class="q-mb-lg">
        <q-item-label header class="text-h4">{{ article.title }}</q-item-label>
        <q-item-label class="text-body1 ellipsis-3-lines text-white">{{
          article.content
        }}</q-item-label>
        <q-btn :to="'/articles/' + article._id" flat label="Подробнее" />
      </q-item-section>
    </q-item>
  </q-list>
</template>
