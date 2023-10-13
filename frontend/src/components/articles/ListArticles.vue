<script setup lang="ts">
import { type ArticleDocument } from '@/client'
import UserItemSection from '@/components/users/UserItemSection.vue'
import { ref } from 'vue'
import { onBeforeMount } from 'vue'
import { DefaultService } from '@/client'

const articles = ref<ArticleDocument[]>([])
const searchText = ref('')
const freezedSearchText = ref('')
const limit = ref<number>(10)
const skip = ref<number>(0)

const loadMoreArticles = async () => {
  const articlesResponse = await DefaultService.listArticlesArticlesGet(
    skip.value,
    limit.value,
    undefined,
    undefined,
    undefined,
    freezedSearchText.value.length > 0 ? freezedSearchText.value : undefined
  )
  articles.value = articlesResponse.articles
}

const handleSearchbarSubmit = async () => {
  articles.value = []
  skip.value = 0
  freezedSearchText.value = searchText.value
  loadMoreArticles()
}

const handleSearchbarClear = () => {
  searchText.value = ''
  freezedSearchText.value = ''
  loadMoreArticles()
}

onBeforeMount(async () => {
  loadMoreArticles()
})
</script>

<template>
  <div class="column items-center bg-secondary">
    <!-- Поисковая строка -->
    <q-input
      v-model="searchText"
      @keyup.enter="handleSearchbarSubmit"
      placeholder="Поиск"
      class="bg-secondary search-input q-py-md q-px-sm"
    >
      <template v-slot:append>
        <q-icon name="search" @click="handleSearchbarSubmit" class="cursor-pointer" />
        <q-icon name="close" @click="handleSearchbarClear" class="cursor-pointer" />
      </template>
    </q-input>
    <!-- Информация о поиске-->
    <div v-if="freezedSearchText.length > 0" class="row self-sta text-info q-mr-md q-mb-lg">
      <div class="q-mr-md">Поисковый запрос: {{ freezedSearchText }}</div>
      <div>Найдено статей: {{ articles.length }}</div>
    </div>

    <!-- Список статей -->
    <q-list separator>
      <q-item
        v-for="article in articles"
        :key="article._id ?? ''"
        class="row items-start bg-secondary"
      >
        <UserItemSection :user="article.author" />

        <q-item-section class="col column items-start">
          <q-item-label header lines="1" class="text-h5">
            <router-link
              style="text-decoration: none; color: inherit"
              :to="'/article/' + article._id"
              >{{ article.title }}</router-link
            >
          </q-item-label>
          <q-item-label
            lines="5"
            class="text-body1 text-white"
            v-html="article.content!.replace(/\n/g, '<br>')"
          />
          <q-btn :to="'/article/' + article._id" flat class="float-right">
            <q-item-label caption class="text-white">Открыть статью полностью >>></q-item-label>
          </q-btn>
        </q-item-section>
      </q-item>
    </q-list>
  </div>
</template>

<style>
.a {
  text-decoration: none;
}

.search-input {
  width: 80%;
}
</style>
