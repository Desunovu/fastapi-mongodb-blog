<script setup lang="ts">
import { ref } from 'vue'
import { DefaultService } from '@/client'
import router from '@/router'

const title = ref('Разработка ПО для платы ESP32')
const tagsString = ref('Программирование, ESP32')
const keyPhrasesString = ref('Среда разработки, Обмен данными')
const loading = ref(false)

const handleSubmit = async () => {
  loading.value = true
  const gptGeneratorResponse = await DefaultService.generateArticleGptWriterPost({
    title: title.value,
    tags: [...tagsString.value.split(','), 'ChatGPT generated'],
    key_phrases: keyPhrasesString.value.split(',').map((phrase) => phrase.trim())
  }).finally(() => {
    loading.value = false
  })

  console.log(gptGeneratorResponse)

  const articleId = gptGeneratorResponse.article._id
  // push по имени компонента и id статьи
  router.push({ name: 'edit-article', params: { id: articleId } })
}
</script>

<template>
  <q-card square class="shadow-24" style="width: 400px; height: 550px">
    <q-card-section class="bg-primary">
      <h4 class="text-white q-my-md">GptWriter</h4>
    </q-card-section>

    <!-- Описание модуля GptWriter -->
    <q-card-section class="bg-primary">
      <p class="text-white">Данный модуль генерирует статью на основе введенных данных.</p>
      <p class="text-white">
        После успешной генерации вы будете перенаправлены на страницу редактирования созданной
        статьи.
      </p>
    </q-card-section>

    <q-form class="q-px-md q-pt-md">
      <q-input label="Заголовок" v-model="title" clearable />
      <!-- Инпут для нового тега -->
      <q-input label="Новые теги (через запятую)" v-model="tagsString" clearable />
      <!-- Инпут для новых ключевых фраз -->
      <q-input label="Новые ключевые фразы (через запятую)" v-model="keyPhrasesString" clearable />
    </q-form>

    <!-- Показывать загрузку пока не получен ответ -->
    <q-card-actions class="q-px-lg">
      <q-btn
        unelevated
        size="lg"
        color="secondary"
        class="full-width text-white"
        @click="handleSubmit"
        :disable="loading"
      >
        <div v-if="!loading" class="row items-center no-wrap">
          <div>Генерировать статью</div>
        </div>
        <q-spinner-oval v-if="loading" />
      </q-btn>
    </q-card-actions>
  </q-card>
</template>
