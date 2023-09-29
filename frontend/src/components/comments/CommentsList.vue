<script setup lang="ts">
import { DefaultService, type CommentDocument } from '@/client'
import UserItemSection from '../users/UserItemSection.vue'
import moment from 'moment'
import { computed, onBeforeMount, ref } from 'vue'
import { useUserStore } from '@/stores/UserStore'
import { Notify } from 'quasar'

const props = defineProps<{
  articleId: string
}>()

const comments = ref<CommentDocument[]>([])
const deletedCommentIds = ref<string[]>([])
const skip = ref<number>(0)
const limit = ref<number>(2)
const newCommentText = ref<string>('')
const newReplyText = ref<string>('')
const commentEditorIsActive = ref<boolean>(false)
const activeReplyEditorCommentId = ref<string | null>(null)

const currentUser = useUserStore().user

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

const loadMore = async (index, done) => {
  const commentsLoaded = await loadMoreComments()
  done(commentsLoaded > 0 ? false : true)
}

const reloadComments = async () => {
  const commentsResponse = await DefaultService.listCommentsCommentsGet(
    props.articleId,
    0,
    skip.value + limit.value
  )
  comments.value = commentsResponse.comments
}

const handleReplyButtonClick = (commentId: string) => {
  activeReplyEditorCommentId.value = commentId
  newReplyText.value = ''
}

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

const handleDeleteCommentButtonClick = async (commentId: string) => {
  await DefaultService.deleteCommentCommentsCommentIdDelete(commentId)
  Notify.create('Комментарий удален')
  deletedCommentIds.value.push(commentId)
}

const checkUserCanModifyComment = (authorId: string) => {
  return currentUser?.role == 'Admin' || currentUser?._id == authorId
}

const isCommentDisabled = (commentId: string) => {
  return deletedCommentIds.value.includes(commentId)
}

onBeforeMount(() => {
  loadMoreComments()
})
</script>

<template>
  <q-list class="column bg-secondary">
    <q-infinite-scroll @load="loadMore" :offset="10">
      <div class="text-h5 text-white q-ml-md q-mt-md">Комментарии</div>
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

      <q-item
        v-for="comment in comments"
        :key="comment._id!"
        :class="{ 'disabled-item': isCommentDisabled(comment._id!) }"
        class="column"
      >
        <div class="row shadow-5 q-pa-xs">
          <UserItemSection small class="self-start" />
          <div class="col items-start">
            <div class="row justify-between items-center">
              <div class="col-grow text-subtitle1">
                @{{ 'username' in comment.author ? comment.author.username : '' }}
              </div>
              <div class="col text-right">
                {{ comment.updated_at ? '(изменено)' : '' }}
                {{ moment(comment.created_at).format('hh:mm DD-MM-YYYY') }}
              </div>
            </div>

            <q-item-section class="text-white">
              {{ comment.content }}
            </q-item-section>

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

        <q-list class="q-ml-xl">
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
          <q-item
            v-for="reply in comment.replies"
            :key="reply._id ?? reply.id"
            :class="{ 'disabled-item': isCommentDisabled(reply._id ?? reply.id) }"
            class="row shadow-2 q-my-xs q-pa-sm"
          >
            <UserItemSection small class="self-start" />
            <div class="col items-start">
              <div class="row justify-between">
                <div class="col">@{{ reply?.author?.username ?? '' }}</div>
                <div class="col-stretch text-right">
                  {{ comment.updated_at ? '(изменено)' : '' }}
                  {{ moment(comment.created_at).format('hh:mm DD-MM-YYYY') }}
                </div>
              </div>
              <div class="text-white">
                {{ reply.content ?? '' }}
              </div>

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
