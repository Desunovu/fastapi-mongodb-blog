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
const tagsRef = ref<string[]>(
  props.articleToEdit?.tags ? props.articleToEdit.tags : ['Тег1', 'Тег2']
)
const previewImageURLRef = ref<string | null>(props.articleToEdit?.preview_image_url ?? null)
const newTag = ref<string>('')

const articleDeleteDialog = ref<boolean>(false)
const previewImageDialog = ref<boolean>(false)

async function handleArticleSave() {
  if (props.createMode) {
    const createArticleResponse = await DefaultService.createArticleArticlesPost({
      title: titleRef.value,
      content: conentRef.value,
      tags: tagsRef.value,
      preview_image_url: previewImageURLRef.value
    })
    Notify.create('Создана новая статья, перенаправляем')
    router.push('/article/' + createArticleResponse.article._id)
  } else if (props.editMode) {
    const updateArticleResponse = await DefaultService.updateArticleArticlesArticleIdPut(
      props.articleToEdit?._id ?? '',
      {
        title: titleRef.value,
        content: conentRef.value,
        tags: tagsRef.value,
        preview_image_url: previewImageURLRef.value
      }
    )
    Notify.create('Cтатья успешно обновлена, перенаправляем')
    router.push('/article/' + updateArticleResponse.article._id)
  }
}

function getDefaultPreviewImages() {
  return [
    'https://as1.ftcdn.net/v2/jpg/02/90/89/76/1000_F_290897614_7RdAsk2GmumcGWZ2qklmV74hKlNmznSx.jpg',
    'https://as2.ftcdn.net/v2/jpg/01/70/93/27/1000_F_170932733_VOHGeaH5AjrVCXBVryEwVgwhArv2wNNH.jpg',
    'https://as1.ftcdn.net/v2/jpg/05/35/47/38/1000_F_535473874_OWCa2ohzXXNZgqnlzF9QETsnbrSO9pFS.jpg',
    'https://as2.ftcdn.net/v2/jpg/02/90/89/76/1000_F_290897614_7RdAsk2GmumcGWZ2qklmV74hKlNmznSx.jpg',
    'https://as1.ftcdn.net/v2/jpg/05/48/56/38/1000_F_548563894_s5tGFJjPhc7lp5uG4iJkR77QbgvrKr9e.jpg'
  ]
}

async function handleArticleDelete() {
  await DefaultService.deleteArticleArticlesArticleIdDelete(props.articleToEdit?._id!)
  Notify.create('Статья удалена')
  router.push('/')
}

function handleAddTag() {
  if (newTag.value) {
    tagsRef.value.push(newTag.value)
    newTag.value = ''
  }
}
</script>

<template>
  <div class="column q-pa-md">
    <q-card square class="shadow-24" style="min-heightht: 550px">
      <!-- Редактор HTML -->
      <q-input
        v-model="titleRef"
        label="Заголовок"
        :input-style="{ fontSize: '20px' }"
        class="q-ma-md"
      />
      <q-editor v-model="conentRef" min-height="5rem" />

      <!-- Ссылка на превью -->
      <div class="row justify-between items-center">
        <q-input v-model="previewImageURLRef" label="Ссылка на превью" class="col-grow q-pa-md" />
        <!-- Высота изрбражения ограничена соседними копонентами-->
          <img :src="previewImageURLRef" class="rounded-borders" style="max-height: 50px" />
        <q-btn
          label="Выбрать превью из стандартных"
          @click="previewImageDialog = true"
          flat
          size="sm"
          class="col-4"
        />
      </div>

      <!-- Теги -->
      <div class="row justify-between items-center">
        <div>
          <q-chip
            v-for="tag in tagsRef"
            :label="tag"
            :key="tag"
            removable
            @remove="tagsRef.splice(tagsRef.indexOf(tag), 1)"
            size="sm"
            dark
            color="primary"
          />
        </div>
        <!-- Добавить тег -->
        <div class="row">
          <q-input v-model="newTag" class="col q-pl-lg" dense />
          <q-btn label="Добавить тег" @click="handleAddTag" flat size="sm"> </q-btn>
        </div>
      </div>

      <!-- Кнопки -->
      <q-card-actions class="row justify-between">
        <q-btn label="Сохранить статью" class="q-ma-md self-stretch" @click="handleArticleSave" />
        <!-- Красная кнопка удалить вызывающая диалог удаления -->
        <q-btn
          v-if="editMode"
          label="Удалить статью"
          class="q-ma-md self-stretch text-white bg-negative"
          @click="articleDeleteDialog = true"
        />
      </q-card-actions>
    </q-card>

    <!-- Диалог подтвержения удаления статьи (Сообщение: вы уверены что хотите удалить статью? Это действие необратимо) -->
    <q-dialog v-model="articleDeleteDialog">
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
    <!-- Диалог выбора превью из стандартных -->
    <q-dialog v-model="previewImageDialog">
      <q-card class="bg-secondary" style="width: 100%">
        <q-card-section class="q-pt-lg">
          <div class="text-center text-h6 text-white q-mb-md">Выберите превью для статьи</div>
          <q-btn
            v-for="imageUrl in getDefaultPreviewImages()"
            :key="imageUrl"
            @click="previewImageURLRef = imageUrl"
            v-close-popup
            flat
          >
            <img :src="imageUrl" style="width: 100px" />
          </q-btn>
        </q-card-section>
      </q-card>
    </q-dialog>
  </div>
</template>
