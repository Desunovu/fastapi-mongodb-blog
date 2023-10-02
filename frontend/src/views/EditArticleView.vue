<script setup lang="ts">
import { type ArticleDocument, DefaultService } from '@/client'
import ArticleEditor from '@/components/articles/ArticleEditor.vue'
import { onBeforeMount, ref } from 'vue'
import { onBeforeRouteUpdate, useRoute } from 'vue-router'

const createMode = ref<boolean>(false)
const editMode = ref<boolean>(false)
const article = ref<ArticleDocument>()

const route = useRoute()

async function resolveView() {
  if (route.path == '/create-article') {
    createMode.value = true
    console.log('Режим создания статьи')
  } else {
    const articleResponse = await DefaultService.readArticleArticlesArticleIdGet(
      route.params.id.toString()
    )
    article.value = articleResponse.article
    editMode.value = true
    console.log('Режим редактирования статьи')
    console.log(article)
  }
}

onBeforeMount(() => {
  resolveView()
})

onBeforeRouteUpdate(() => {
  resolveView()
})
</script>

<template>
  <q-page padding>
    <ArticleEditor v-if="createMode" create-mode />
    <ArticleEditor v-if="editMode" edit-mode :article-to-edit="article" />
  </q-page>
</template>
