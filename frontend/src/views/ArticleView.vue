<script setup lang="ts">
import { DefaultService, type ArticleDocument, type CommentDocument } from '@/client'
import SingleArticle from '@/components/articles/SingleArticle.vue'
import CommentsList from '@/components/comments/CommentsList.vue';
import { onBeforeMount, onMounted, ref } from 'vue'
import { useRoute } from 'vue-router'

const article = ref<ArticleDocument>()

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
    <SingleArticle v-if="article" :article="article" />
    <CommentsList v-if="article" :articleId="article?._id!"/>
  </q-page>
</template>
