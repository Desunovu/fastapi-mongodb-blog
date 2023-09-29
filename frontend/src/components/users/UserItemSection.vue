<script setup lang="ts">
import { computed } from 'vue'

export interface Props {
  small?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  small: () => false
})

const avatarSize = computed(() => {
  return props.small ? '50px' : '100px'
})

const sectionWidth = computed(() => {
  return props.small ? '70px' : '20%'
})
</script>

<template>
  <q-item-section
    avatar
    class="column items-center justify-start"
    :style="{ 'min-width': sectionWidth, 'max-width': sectionWidth }"
  >
    <q-avatar :size="avatarSize" rounded>
      <img src="https://cdn.quasar.dev/img/boy-avatar.png" />
    </q-avatar>
    <q-item-label v-if="!small" class="text-body ellipsis text-white">
      Лололошка | Официальный канал
    </q-item-label>
  </q-item-section>
</template>
