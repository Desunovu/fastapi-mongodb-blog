<script setup lang="ts">
import { DefaultService, type ArticleDocument } from '@/client'
import ListArticles from '@/components/articles/ListArticles.vue'
import { onMounted, ref } from 'vue'

const articles = ref<ArticleDocument[]>([])

onMounted(async () => {
  const articlesResponse = await DefaultService.listArticlesArticlesGet()
  articles.value = articlesResponse.articles
})
</script>

<template>
  <q-page padding>
    <ListArticles :articles="articles" />
  </q-page>
</template>
