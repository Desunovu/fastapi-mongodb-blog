<script setup lang="ts">
import { type ArticleDocument } from '@/client'
import UserItemSection from '@/components/users/UserItemSection.vue'

const props = defineProps({
  articles: Array<ArticleDocument>
})
</script>

<template>
  <q-list separator>
    <q-item
      v-for="article in articles"
      :key="article._id ?? ''"
      class="row items-start bg-secondary"
    >
      <UserItemSection />

      <q-item-section class="col column items-start">
        <q-item-label header lines="1" class="text-h5">
          <router-link
            style="text-decoration: none; color: inherit"
            :to="'/article/' + article._id"
            >{{ article.title }}</router-link
          >
        </q-item-label>
        <q-item-label lines="5" class="text-body1 text-white">{{ article.content }}</q-item-label>
        <q-btn :to="'/article/' + article._id" flat class="float-right">
          <q-item-label caption class="text-white">Открыть статью полностью >>></q-item-label>
        </q-btn>
      </q-item-section>
    </q-item>
  </q-list>
</template>

<style>
.a {
  text-decoration: none;
}
</style>
