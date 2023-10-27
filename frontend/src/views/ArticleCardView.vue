<script setup lang="ts">
import { DefaultService, type ArticleDocumentResponse } from '@/client'
import ArticleCard from '@/components/ArticleCard.vue'
import CommentList from '@/components/CommentList.vue'
import { onBeforeMount, ref } from 'vue'
import { useRoute } from 'vue-router'

const article = ref<ArticleDocumentResponse>()

const route = useRoute()

const loadArticle = async () => {
  const articleResponse = await DefaultService.readArticleArticlesArticleIdGet(
    route.params.id.toString()
  )
  article.value = articleResponse.article
}

onBeforeMount(async () => {
  await loadArticle()
})
</script>

<template>
  <q-page padding>
    <ArticleCard v-if="article" :article="article" />
    <CommentList v-if="article" :articleId="article?._id!" />
  </q-page>
</template>
