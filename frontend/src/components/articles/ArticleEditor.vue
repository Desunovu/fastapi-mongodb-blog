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
const articleDeleteDialog = ref<boolean>(false)

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
      { title: titleRef.value, content: conentRef.value }
    )
    Notify.create('Cтатья успешно обновлена, перенаправляем')
    router.push('/article/' + updateArticleResponse.article._id)
  }
}

async function handleArticleDelete() {
  await DefaultService.deleteArticleArticlesArticleIdDelete(props.articleToEdit?._id!)
  Notify.create('Статья удалена')
  router.push('/')
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
      <q-card-actions class="row justify-between">
        <q-btn label="Сохранить статью" class="q-ma-md self-stretch" @click="handleArticleSave" />
        <!-- Красная кнопка удалить вызывающая диалог удаления -->
        <q-btn
          :if="editMode"
          label="Удалить статью"
          class="q-ma-md self-stretch bg-negative"
          @click="articleDeleteDialog = true"
        />
      </q-card-actions>
    </q-card>

    <q-dialog v-model="articleDeleteDialog">
      <!-- Диалог подтвержения удаления статьи (Сообщение: вы уверены что хотите удалить статью? Это действие необратимо) -->
      <q-card class="bg-secondary items-center" style="width: 100%">
        <q-card-section>
          <div class="text-body2 text-center q-mt-sm">
            Вы уверены что хотите удалить статью?<br />
            Это действие <b class="text-info">необратимо</b>.
          </div>
        </q-card-section>
        <q-card-actions class="justify-around">
          <q-btn @click="articleDeleteDialog = false" color="primary">Не удалять</q-btn>
          <q-btn @click="handleArticleDelete" color="secondary">Удалить</q-btn>
        </q-card-actions>
      </q-card>
    </q-dialog>
  </div>
</template>
