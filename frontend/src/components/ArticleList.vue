<script setup lang="ts">
import { type ArticleDocumentResponse } from '@/client'
import UserInfoCard from '@/components/UserInfoCard.vue'
import { ref } from 'vue'
import { onBeforeMount } from 'vue'
import { DefaultService } from '@/client'
import { onBeforeRouteUpdate, useRoute } from 'vue-router'
import moment from 'moment'

const route = useRoute()

const articles = ref<ArticleDocumentResponse[]>([])
const searchText = ref('')
const freezedSearchText = ref('')
const limit = ref<number>(10)
const skip = ref<number>(0)
const page = ref<number>(1)
const maxPage = ref<number>(10)
const total = ref<number>(0)
const searchByTags = ref<boolean>(false)

const loadMoreArticles = async () => {
  console.debug('Загрузка статей', skip.value, limit.value)
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
  console.debug('Отправка строки поиска', searchText.value)
  articles.value = []
  skip.value = 0
  freezedSearchText.value = searchText.value
  loadMoreArticles()
}

const handleSearchbarClear = () => {
  console.debug('Сброс поиска')
  searchText.value = ''
  freezedSearchText.value = ''
  loadMoreArticles()
}

const handlePageChange = async () => {
  if (!page.value) {
    page.value = 1
    return
  }
  console.debug('Смена страницы на ', page.value)
  skip.value = (page.value - 1) * limit.value
  await loadMoreArticles()
  window.scrollTo(0, 0)
}

onBeforeMount(async () => {
  if (route.query.tag) {
    console.debug('Монтируется компонент с тегом', route.query.tag)
    searchByTags.value = true
    searchText.value = route.query.tag as string
    await handleSearchbarSubmit()
  } else {
    console.debug('Монтируется компонент без тега')
    await loadMoreArticles()
  }
})

onBeforeRouteUpdate(async (to, from) => {
  window.scrollTo(0, 0)
  articles.value = []
  skip.value = 0

  if (to.query.tag) {
    console.debug('Обновлен компонент с тегом', to.query.tag)
    searchByTags.value = true
    searchText.value = to.query.tag as string
    freezedSearchText.value = searchText.value
    await handleSearchbarSubmit()
  } else {
    console.debug('Обновлен компонент без тега')
    searchByTags.value = false
    searchText.value = ''
    freezedSearchText.value = ''
    await loadMoreArticles()
  }
})
</script>

<template>
  <div class="column bg-secondary q-pa-md">
    <!-- Header -->
    <div class="row justify-end">
      <div class="col-10">
        <!-- Поисковая строка -->
        <q-input
          v-model="searchText"
          @keyup.enter="handleSearchbarSubmit"
          placeholder="Поиск"
          class="col-9 bg-secondary self-end"
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
      </div>
    </div>

    <!-- Список статей -->
    <q-list separator padding>
      <!-- Статья -->
      <div v-for="article in articles" :key="article._id ?? ''" class="row q-mb-lg">
        <!-- Аватар и имя автора -->
        <div class="col-auto q-mx-md">
          <UserInfoCard :user="article.author" class="self-center" />
        </div>

        <!-- Тело статьи -->
        <div class="col column shadow-4 q-pa-sm">
          <!-- HEADER - NO PREVIEW -->
          <div v-if="!article.preview_image_url" class="row justify-between q-mb-md full-width">
            <!-- Заголовок статьи -->
            <div class="col text-h5 text-white text-weight-bold">
              <router-link
                style="color: inherit; align-self: start"
                :to="'/article/' + article._id"
              >
                {{ article.title }}
              </router-link>
            </div>
            <!-- Дата и теги -->
            <div class="col column items-end full-width ">
              <q-item-label caption class="text-body flex-shrink">
                {{ moment(article?.created_at).format('Do MMMM YYYY') }}
              </q-item-label>
              <div v-if="article?.tags">
                <router-link
                  v-for="tag in article?.tags"
                  :key="tag"
                  :to="{ name: 'home', query: { tag: tag } }"
                >
                  <q-chip :label="tag" size="sm" dark color="primary" />
                </router-link>
              </div>
            </div>
          </div>

          <!-- Если есть превью -->
          <div v-else class="q-mb-md rounded-borders" style="position: relative">
            <img
              v-if="article?.preview_image_url"
              :src="article.preview_image_url"
              :alt="article.title ?? ''"
              class="rounded-borders"
              style="width: 100%; height: 250px; object-fit: cover"
            />
            <!-- Оверлей текст -->
            <div class="overlay-text column justify-between q-mb-md">
              <!-- Дата и теги -->
              <div class="col full-width full-height q-pt-md">
                <q-item-label caption class="text-body flex-shrink">
                  {{ moment(article?.created_at).format('Do MMMM YYYY') }}
                </q-item-label>
                <div v-if="article?.tags">
                  <router-link
                    v-for="tag in article?.tags"
                    :key="tag"
                    :to="{ name: 'home', query: { tag: tag } }"
                  >
                    <q-chip :label="tag" size="sm" dark color="primary" />
                  </router-link>
                </div>
              </div>
              <!-- Заголовок статьи -->
              <div class="col full-width full-height text-h3 text-white text-weight-bold">
                <router-link
                  style="color: inherit; align-self: start; text-decoration: none"
                  :to="'/article/' + article._id"
                >
                  {{ article.title }}
                </router-link>
              </div>
              <div class="col full-width full-height"></div>
            </div>
          </div>

          <!-- Контент статьи -->
          <q-item-label
            lines="5"
            class="text-body1 text-white"
            v-html="article.content!.replace(/\n/g, '<br>')"
          />
          <!-- Кнопка "Открыть статью полностью -->
          <q-btn :to="'/article/' + article._id" flat class="float-right">
            <q-item-label caption class="text-white">Открыть статью полностью >>></q-item-label>
          </q-btn>
        </div>
      </div>
    </q-list>

    <!-- Пагинация -->
    <q-pagination
      v-model="page"
      @update:model-value="handlePageChange"
      input
      :max="maxPage"
      class="self-center"
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

.overlay-text {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-weight: bold;
  text-align: center;
  z-index: 1;
  text-shadow: 2px 2px 2px #00000044;
}
</style>
