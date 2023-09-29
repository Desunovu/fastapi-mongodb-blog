<script setup lang="ts">
import { DefaultService, type CommentDocument } from '@/client'
import UserItemSection from '../users/UserItemSection.vue'
import moment from 'moment'
import { onBeforeMount, ref } from 'vue'
import { useUserStore } from '@/stores/UserStore'
import { Notify } from 'quasar'

// Определение пропсов
const props = defineProps<{
  articleId: string
}>()

// Стейт компонента
const comments = ref<CommentDocument[]>([])
const deletedCommentIds = ref<string[]>([])
const skip = ref<number>(0)
const limit = ref<number>(2)
const newCommentText = ref<string>('')
const newReplyText = ref<string>('')
const commentEditorIsActive = ref<boolean>(false)
const activeReplyEditorCommentId = ref<string | null>(null)

// Текущий пользователь из хранилища
const currentUser = useUserStore().user

// Функция для загрузки дополнительных комментариев
const loadMoreComments = async () => {
  const commentsResponse = await DefaultService.listCommentsCommentsGet(
    props.articleId,
    skip.value,
    limit.value
  )
  comments.value.push(...commentsResponse.comments)
  skip.value += limit.value
  return commentsResponse.comments.length
}

// Функция для загрузки комментариев при прокрутке списка комментариев
const loadMore = async (_index: number, done: CallableFunction) => {
  const commentsLoaded = await loadMoreComments()
  done(commentsLoaded > 0 ? false : true)
}

// Функция для перезагрузки списка комментариев
const reloadComments = async () => {
  const commentsResponse = await DefaultService.listCommentsCommentsGet(
    props.articleId,
    0,
    skip.value + limit.value
  )
  comments.value = commentsResponse.comments
}

// Функция для обработки нажатия на кнопку "Ответить"
const handleReplyButtonClick = (commentId: string) => {
  activeReplyEditorCommentId.value = commentId
  newReplyText.value = ''
}

// Функция для отправки нового комментария
const handleCommentSubmit = async () => {
  if (newCommentText.value.length > 0) {
    const commentResponse = await DefaultService.createCommentCommentsPost({
      article_id: props.articleId,
      content: newCommentText.value
    })
    newCommentText.value = ''
    commentEditorIsActive.value = false
    reloadComments()
  }
}

// Функция для отправки нового ответа
const handleReplySubmit = async (commentId: string) => {
  if (newReplyText.value.length > 0) {
    const replyResponse = await DefaultService.createReplyCommentsReplyPost({
      parent_comment_id: commentId,
      content: newReplyText.value
    })
    newReplyText.value = ''
    activeReplyEditorCommentId.value = null
    reloadComments()
  }
}

// Функция для обработки нажатия на кнопку удаления комментария
const handleDeleteCommentButtonClick = async (commentId: string) => {
  await DefaultService.deleteCommentCommentsCommentIdDelete(commentId)
  Notify.create('Комментарий удален')
  deletedCommentIds.value.push(commentId)
}

// Функция для проверки, может ли пользователь изменить комментарий
const checkUserCanModifyComment = (authorId: string) => {
  return currentUser?.role == 'Admin' || currentUser?._id == authorId
}

// Функция для проверки, удален ли комментарий
const isCommentDisabled = (commentId: string) => {
  return deletedCommentIds.value.includes(commentId)
}

onBeforeMount(() => {
  loadMoreComments()
})
</script>

<template>
  <!-- Комментарии к статье и форма добавления нового комментария -->
  <q-list class="column bg-secondary">
    <!-- Бесконечная прокрутка для загрузки дополнительных комментариев -->
    <q-infinite-scroll @load="loadMore" :offset="10">
      <div class="text-h5 text-white q-ml-md q-mt-md">Комментарии</div>

      <!-- Форма добавления нового комментария -->
      <div class="row q-mx-md q-mb-md q-pa-sm shadow-2 text-white">
        <q-input
          v-model="newCommentText"
          @focus="commentEditorIsActive = true"
          label="Добавить новый комментарий..."
          label-color="white"
          class="col-grow q-pa-sm"
        />
        <q-btn
          v-if="commentEditorIsActive"
          @click="handleCommentSubmit"
          label="Отправить"
          class="col-shrink self-center"
        />
      </div>

      <!-- Отображение комментариев -->
      <q-item
        v-for="comment in comments"
        :key="comment._id!"
        :class="{ 'disabled-item': isCommentDisabled(comment._id!) }"
        class="column"
      >
        <div class="row shadow-5 q-pa-xs">
          <UserItemSection small class="self-start" />
          <div class="col items-start">
            <!-- Информация об авторе комментария и времени его создания -->
            <div class="row justify-between items-center">
              <div class="col-grow text-subtitle1">
                @{{ 'username' in comment.author ? comment.author.username : '' }}
              </div>
              <div class="col text-right">
                {{ comment.updated_at ? '(изменено)' : '' }}
                {{ moment(comment.created_at).format('hh:mm DD-MM-YYYY') }}
              </div>
            </div>

            <!-- Текст комментария -->
            <q-item-section class="text-white">
              {{ comment.content }}
            </q-item-section>

            <!-- Кнопки для ответа на комментарий и удаления комментария -->
            <div class="row justify-between">
              <q-btn
                @click="handleReplyButtonClick(comment._id!)"
                label="Ответить"
                color="secondary"
                no-caps
                flat
                padding="none"
                text-color="white"
                align="left"
              />
              <q-btn
                v-if="checkUserCanModifyComment(comment.author._id ?? comment.author.id)"
                @click="handleDeleteCommentButtonClick(comment._id! ?? comment._id)"
                label="Удалить"
                icon-right="clear"
                no-caps
                flat
                padding="none"
              />
            </div>
          </div>
        </div>

        <!-- Отображение ответов -->
        <q-list class="q-ml-xl">
          <!-- Форма добавления ответа на комментарий -->
          <div
            v-if="activeReplyEditorCommentId === comment._id"
            class="row shadow-2 q-my-xs q-pa-sm text-white"
          >
            <q-input
              v-model="newReplyText"
              label="Добавить ответ..."
              label-color="white"
              class="col-grow q-px-sm"
            />
            <q-btn
              @click="handleReplySubmit(comment._id!)"
              label="Отправить"
              class="col-shrink self-center"
            />
          </div>

          <!-- Отображение ответов на комментарий -->
          <q-item
            v-for="reply in comment.replies"
            :key="reply._id ?? reply.id!"
            :class="{ 'disabled-item': isCommentDisabled(reply._id ?? reply.id) }"
            class="row shadow-2 q-my-xs q-pa-sm"
          >
            <UserItemSection small class="self-start" />
            <div class="col items-start">
              <!-- Информация об авторе ответа и времени его создания -->
              <div class="row justify-between">
                <div class="col">@{{ reply.author.username ?? '' }}</div>
                <div class="col-stretch text-right">
                  {{ comment.updated_at ? '(изменено)' : '' }}
                  {{ moment(comment.created_at).format('hh:mm DD-MM-YYYY') }}
                </div>
              </div>

              <!-- Текст ответа -->
              <div class="text-white">
                {{ reply.content ?? '' }}
              </div>

              <!-- Кнопка для удаления ответа -->
              <div class="row justify-end">
                <q-btn
                  v-if="checkUserCanModifyComment(reply.author._id ?? reply.author.id)"
                  @click="handleDeleteCommentButtonClick(reply._id ?? reply.id)"
                  label="Удалить"
                  icon-right="clear"
                  no-caps
                  flat
                  padding="none"
                />
              </div>
            </div>
          </q-item>
        </q-list>
      </q-item>
    </q-infinite-scroll>
  </q-list>
</template>

<style>
.disabled-item {
  pointer-events: none; /* Отключает взаимодействие с q-item и его дочерними элементами */
  opacity: 0.5; /* Может быть использовано для затемнения отключенных элементов */
}
</style>
