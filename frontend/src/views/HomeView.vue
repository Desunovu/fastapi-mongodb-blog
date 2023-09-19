<script setup lang="ts">
import { DefaultService, type ArticleDocument } from '@/client'
import ListArticles from '@/components/articles/ListArticles.vue'
import { onMounted, ref } from 'vue'

const articles = ref<ArticleDocument[]>([])
const current_page = ref(1)

onMounted(async () => {
  const articlesResponse = await DefaultService.listArticlesArticlesGet()
  articles.value = articlesResponse.articles
  console.log(articles)
})
</script>

<template>
  <main>
    <ListArticles :articles="articles" class="q-px-lg"/>
    <div class="q-pa-lg flex flex-center">
      <q-pagination
        v-model="current_page"
        color="black"
        :max="1"
        :max-pages="6"
        :boundary-numbers="false"
      />
    </div>
  </main>
</template>
