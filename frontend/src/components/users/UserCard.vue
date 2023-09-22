<script setup lang="ts">
import { DefaultService, type UserDocument } from '@/client'
import AuthService from '@/services/AuthService'
import { beforeEach } from 'node:test'
import { Notify } from 'quasar'
import { ref } from 'vue'

export interface Props {
  user: UserDocument | undefined
  editable?: boolean
  isProfile?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  isProfile: () => false,
  editable: () => false
})

const emailDialog = ref(false)
const passwordDialog = ref(false)
const newEmail = ref()
const newPassword = ref()
const oldPassword = ref()

async function handleEmailUpdate() {
  const updateEmailResponse = await DefaultService.updateUserUsersUserIdPut(props.user?._id ?? '', {
    email: newEmail.value
  })
  Notify.create('Установлен E-mail: ' + updateEmailResponse.user.email)
  // TODO Вызвать ре-рендер родительского компонента

  if (props.isProfile) {
    AuthService.update_user_info()
  }
}

async function handlePasswordUpdate() {
  const updatePasswordResponse = await DefaultService.updateUserPasswordUsersUserIdPasswordPut(
    props?.user?._id ?? '',
    { old_password: oldPassword.value, new_password: newPassword.value }
  )
  Notify.create('Установлен новый пароль!')
}
</script>

<template>
  <q-item class="row justify-start items-start q-pt-lg bg-secondary">
    <q-item-section class="col-shrink column items-center">
      <q-avatar size="150px" rounded>
        <img src="https://cdn.quasar.dev/img/boy-avatar.png" />
      </q-avatar>
      <q-item-label class="text-body1 text-white">{{ user?.role }}</q-item-label>
      <q-item-label v-if="user?.disabled" caption class="text-white">ЗАБЛОКИРОВАН</q-item-label>
    </q-item-section>

    <q-item-section class="col-grow column" style="overflow: auto">
      <q-item-label class="text-h3 text-info">{{ user?.username }}</q-item-label>
      <q-item-label class="text-h6 text-white">{{ user?.email }}</q-item-label>
      <q-btn
        v-if="editable"
        label="Изменить E-mail"
        @click="emailDialog = true"
        class="self-stretch"
        align="left"
        flat
      />
      <q-btn
        v-if="editable"
        label="Изменить пароль"
        @click="passwordDialog = true"
        class="self-stretch"
        align="left"
        flat
      />
    </q-item-section>

    <q-dialog v-model="emailDialog">
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

    <q-dialog v-model="passwordDialog">
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
  </q-item>
</template>
s
