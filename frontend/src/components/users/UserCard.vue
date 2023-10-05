<script setup lang="ts">
import { DefaultService, type UserDocument } from '@/client'
import AuthService from '@/services/AuthService'
import { Notify } from 'quasar'
import { ref } from 'vue'
import UserItemSection from './UserItemSection.vue'

export interface Props {
  user?: UserDocument | null
  editable?: boolean
  isProfile?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  isProfile: () => false,
  editable: () => false
})

const showEmailDialog = ref(false)
const showPasswordDialog = ref(false)
const showAvatarDialog = ref(false)
const newEmail = ref<string>()
const newPassword = ref<string>('')
const oldPassword = ref<string>('')
const avatarsToChoose = ref<string[]>([])

async function loadAvatarsToChoose() {
  const avatarsResponse = {
    avatars: [
      'https://cdn-icons-png.flaticon.com/512/149/149071.png',
      'https://cdn-icons-png.flaticon.com/512/149/149072.png',
      'https://cdn-icons-png.flaticon.com/512/149/149074.png'
    ]
  }
  avatarsToChoose.value = avatarsResponse.avatars
}

async function handleAvatarUpdate(avatarUrl: string) {
  const updateAvatarResponse = await DefaultService.updateUserUsersUserIdPut(
    props.user._id ?? props.user.id,
    {
      avatar_url: avatarUrl
    }
  )
  Notify.create(
    'Установлен аватар: ' + updateAvatarResponse.user.avatar_url + '. Перезагрузите страницу'
  )
}

async function prepareAvatarDialog() {
  showAvatarDialog.value = true
  await loadAvatarsToChoose()
}

async function handleEmailUpdate() {
  const updateEmailResponse = await DefaultService.updateUserUsersUserIdPut(
    props.user._id ?? props.user.id,
    {
      email: newEmail.value
    }
  )
  Notify.create('Установлен E-mail: ' + updateEmailResponse.user.email + '. Перезагрузите страницу')

  if (props.isProfile) {
    AuthService.update_user_info()
  }
}

async function handlePasswordUpdate() {
  await DefaultService.updateUserPasswordUsersUserIdPasswordPut(props.user._id ?? props.user.id, {
    old_password: oldPassword.value,
    new_password: newPassword.value
  })
  Notify.create('Установлен новый пароль!')
}
</script>

<template>
  <q-item class="row justify-start items-start q-pt-lg bg-secondary">
    <UserItemSection :user="user" class="col" />
    <q-item-section class="col-grow items-start" style="overflow: auto">
      <q-item-label lines="1" class="text-h5 text-white">
        {{ user?.email }}
      </q-item-label>
      <q-item-label class="text-caption text-white">
        ***Раздел для прочей информации о пользователе***
      </q-item-label>
    </q-item-section>
    <q-item-section class="col-4" style="overflow: auto">
      <q-btn
        v-if="editable"
        label="Изменить E-mail"
        @click="showEmailDialog = true"
        class="self-stretch"
        align="left"
        flat
      />
      <q-btn
        v-if="editable"
        label="Изменить пароль"
        @click="showPasswordDialog = true"
        class="self-stretch"
        align="left"
        flat
      />

      <q-btn
        v-if="editable"
        label="Изменить аватар"
        @click="prepareAvatarDialog"
        class="self-stretch"
        align="left"
        flat
      />
    </q-item-section>

    <q-dialog v-model="showEmailDialog">
      <q-card class="bg-secondary" style="width: 100%">
        <q-card-section class="q-pt-lg">
          <q-input
            v-model="newEmail"
            label="Новый Email"
            clearable
            :input-style="{ fontSize: '25px' }"
          />
        </q-card-section>

        <q-card-actions align="center" class="bg-secondary text-teal">
          <q-btn label="Изменить" @click="handleEmailUpdate" v-close-popup flat />
        </q-card-actions>
      </q-card>
    </q-dialog>

    <q-dialog v-model="showPasswordDialog">
      <q-card class="bg-secondary" style="width: 100%">
        <q-card-section class="q-pt-lg">
          <q-input
            v-model="oldPassword"
            label="Старый пароль"
            v-if="isProfile"
            clearable
            :input-style="{ fontSize: '25px' }"
          />
          <q-input
            v-model="newPassword"
            label="Новый пароль"
            clearable
            :input-style="{ fontSize: '25px' }"
          />
        </q-card-section>

        <q-card-actions align="center" class="bg-secondary text-teal">
          <q-btn label="Изменить" @click="handlePasswordUpdate" v-close-popup flat />
        </q-card-actions>
      </q-card>
    </q-dialog>

    <q-dialog v-model="showAvatarDialog">
      <q-card class="bg-secondary" style="width: 100%">
        <q-card-section class="q-pt-lg">
          <!-- Надпись по центру "выберите аватар" -->
          <div class="text-center text-h6 text-white q-mb-md">Выберите аватар</div>
          <q-btn
            v-for="avatarUrl in [...avatarsToChoose, ...avatarsToChoose, ...avatarsToChoose]"
            :key="avatarUrl"
            @click="handleAvatarUpdate(avatarUrl)"
            v-close-popup
            flat
          >
            <img :src="avatarUrl" style="width: 100px" />
          </q-btn>
        </q-card-section>
      </q-card>
    </q-dialog>
  </q-item>
</template>
