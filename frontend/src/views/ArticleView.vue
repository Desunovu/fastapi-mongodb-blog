<script setup lang="ts">
import { DefaultService, type ArticleDocument } from '@/client'
import SingleArticle from '@/components/articles/SingleArticle.vue'
import { onMounted, ref } from 'vue'
import { useRoute } from 'vue-router'

const article = ref<ArticleDocument>()

const route = useRoute()

onMounted(async () => {
  const articleResponse = await DefaultService.readArticleArticlesArticleIdGet(
    route.params.id.toString()
  )
  article.value = articleResponse.article
})
</script>

<template>
  <q-page padding>
    <SingleArticle v-if="article" :article="article" />
  </q-page>
</template>
