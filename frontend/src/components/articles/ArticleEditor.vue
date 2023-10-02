<script setup lang="ts">
import { DefaultService, type ArticleDocument } from '@/client'
import router from '@/router'
import { Notify } from 'quasar'
import { ref } from 'vue'

export interface Props {
  articleToEdit?: ArticleDocument
  createMode?: boolean
  editMode?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  createMode: () => false,
  editMode: () => false
})

const titleRef = ref<string>(
  props.articleToEdit?.title ? props.articleToEdit.title : 'Заголовок статьи'
)
const conentRef = ref<string>(
  props.articleToEdit?.content ? props.articleToEdit.content : 'Текст статьи'
)

async function handleArticleSave() {
  if (props.createMode) {
    const createArticleResponse = await DefaultService.createArticleArticlesPost({
      title: titleRef.value,
      content: conentRef.value
    })
    Notify.create('Создана новая статья, перенаправляем')
    router.push('/article/' + createArticleResponse.article._id)
  } else if (props.editMode) {
    const updateArticleResponse = await DefaultService.updateArticleArticlesArticleIdPut(
      props.articleToEdit?._id ?? '',
      { title: titleRef.value, content: conentRef.value}
    )
    Notify.create('Cтатья успешно обновлена, перенаправляем')
    router.push('/article/' + updateArticleResponse.article._id)
  }
}
</script>

<template>
  <div class="column q-pa-md">
    <q-card square class="shadow-24" style="min-heightht: 550px">
      <q-input
        v-model="titleRef"
        label="Заголовок"
        :input-style="{ fontSize: '20px' }"
        class="q-ma-md"
      />
      <q-editor v-model="conentRef" min-height="5rem" />

      <q-btn label="Сохранить статью" class="q-ma-md self-stretch" @click="handleArticleSave" />

      <!-- <q-card flat bordered>
      <q-card-section>
        <pre style="white-space: pre-line">{{ editor }}</pre>
      </q-card-section>
    </q-card>

    <q-card flat bordered>
      <div v-html="editor" />
    </q-card> -->
    </q-card>
  </div>
</template>
