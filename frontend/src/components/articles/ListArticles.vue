<script setup lang="ts">
import { type ArticleDocument } from '@/client'
import UserItemSection from '@/components/users/UserItemSection.vue'
import { ref } from 'vue'
import { onBeforeMount } from 'vue'
import { DefaultService } from '@/client'
import { onBeforeRouteUpdate, useRoute } from 'vue-router'

const route = useRoute()

const articles = ref<ArticleDocument[]>([])
const searchText = ref('')
const freezedSearchText = ref('')
const limit = ref<number>(10)
const skip = ref<number>(0)
const page = ref<number>(1)
const maxPage = ref<number>(10) // TODO получать из ответа сервера
const total = ref<number>(0)
const searchByTags = ref<boolean>(false)

const loadMoreArticles = async () => {
  const searchInput = freezedSearchText.value.length > 0 ? freezedSearchText.value : undefined

  const articlesResponse = await DefaultService.listArticlesArticlesGet(
    skip.value,
    limit.value,
    undefined,
    undefined,
    searchByTags.value ? searchInput : undefined, // tag
    !searchByTags.value ? searchInput : undefined // searchQuery
  )
  articles.value = articlesResponse.articles
  total.value = articlesResponse.total
  maxPage.value = Math.ceil(total.value / limit.value)
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

const handlePageChange = async () => {
  skip.value = (page.value - 1) * limit.value
  await loadMoreArticles()
  window.scrollTo(0, 0)
}

onBeforeMount(async () => {
  if (route.query.tag) {
    searchByTags.value = true
    searchText.value = route.query.tag as string
    await handleSearchbarSubmit()
  } else {
    await loadMoreArticles()
  }
})

onBeforeRouteUpdate(async (to, from) => {
  window.scrollTo(0, 0)
  articles.value = []
  skip.value = 0

  if (to.query.tag) {
    searchByTags.value = true
    searchText.value = to.query.tag as string
    freezedSearchText.value = searchText.value
    await handleSearchbarSubmit()
  } else {
    searchByTags.value = false
    searchText.value = ''
    freezedSearchText.value = ''
    await loadMoreArticles()
  }
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
      <!-- Чекбокс "искать по тегам" -->
      <q-checkbox
        v-model="searchByTags"
        label="Искать по тегам"
        class="q-mr-sm"
        @update:model-value="handleSearchbarSubmit"
      />
    </q-input>
    <!-- Информация о поиске-->
    <div v-if="freezedSearchText.length > 0" class="row self-sta text-info q-mr-md q-mb-lg">
      <div class="q-mr-md">Поисковый запрос: {{ freezedSearchText }}</div>
      <div>Найдено статей: {{ total }}</div>
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

          <!-- Теги -->
          <div v-if="article?.tags">
            <router-link
              v-for="tag in article?.tags"
              :key="tag"
              :to="{ name: 'home', query: { tag: tag } }"
            >
              <q-chip :label="tag" size="sm" dark color="primary" />
            </router-link>
          </div>

          <!-- Открытие статьи -->
          <q-btn :to="'/article/' + article._id" flat class="float-right">
            <q-item-label caption class="text-white">Открыть статью полностью >>></q-item-label>
          </q-btn>
        </q-item-section>
      </q-item>
    </q-list>

    <!-- Пагинация -->
    <q-pagination
      v-model="page"
      @update:model-value="handlePageChange"
      input
      :max="maxPage"
      class="q-my-lg"
    />
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
