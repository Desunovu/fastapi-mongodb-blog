<script setup lang="ts">
import type { UserDocument } from '@/client'
import { computed } from 'vue'

export interface Props {
  user?: UserDocument | null
  small?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  small: () => false
})

const avatarSizeStyle = computed(() => {
  return props.small ? '50px' : '100px'
})

const sectionWidthStyle = computed(() => {
  return props.small ? '70px' : '20%'
})
</script>

<template>
  <q-item-section
    v-if="user"
    avatar
    class="column items-center justify-start"
    :style="{ 'min-width': sectionWidthStyle, 'max-width': sectionWidthStyle }"
  >
    <q-avatar :size="avatarSizeStyle" rounded>
      <q-img :src="user?.avatar_url!" />
    </q-avatar>

    <template v-if="!props.small">
      <q-item-label
        lines="1"
        class="text-subtitle1 text-uppercase text-white text-weight-bold q-my-sm"
      >
        {{ user?.username }}
      </q-item-label>
      <q-item-label lines="1" class="text-subtitle2 text-white text-weight-bold q-my-sm">
        <span v-if="user?.role == 'Author'" class="text-blue">Автор</span>
        <span v-else-if="user?.role == 'Admin'" class="text-red">Администратор</span>
      </q-item-label></template
    >
  </q-item-section>
</template>
