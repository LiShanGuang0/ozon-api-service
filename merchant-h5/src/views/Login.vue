<script setup lang="ts">
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { KeyRound, LogIn, ShieldCheck } from 'lucide-vue-next'
import { ElMessage } from 'element-plus'

import { bootstrapMerchant } from '../api/merchant'
import { useI18n } from '../i18n'
import { useMerchantStore } from '../stores/merchant'

const router = useRouter()
const merchant = useMerchantStore()
const { t } = useI18n()
const loading = ref(false)

const form = reactive({
  clientId: merchant.clientId,
  apiKey: '',
})

async function submit() {
  if (!form.clientId || !form.apiKey) {
    ElMessage.warning(t('credentialRequired'))
    return
  }

  loading.value = true
  try {
    const result = await bootstrapMerchant({
      client_id: form.clientId,
      api_key: form.apiKey,
    })
    merchant.setCredentials(result.profile.client_id, form.apiKey)
    ElMessage.success(result.initialized_from_ozon ? t('initializedFromOzon') : t('credentialPassed'))
    router.replace('/dashboard')
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <main class="login-page">
    <section class="login-card">
      <div class="login-brand">
        <div class="brand-mark">
          <KeyRound :size="24" />
        </div>
        <div>
          <strong>{{ t('loginBrand') }}</strong>
          <span>{{ t('loginSubtitle') }}</span>
        </div>
      </div>

      <div class="login-title">
        <span>
          <ShieldCheck :size="16" />
          {{ t('credentialLogin') }}
        </span>
        <h1>{{ t('connectShop') }}</h1>
        <p>{{ t('loginDesc') }}</p>
      </div>

      <el-form label-position="top" @submit.prevent="submit">
        <el-form-item label="Client-Id">
          <el-input v-model="form.clientId" size="large" :placeholder="t('clientIdPlaceholder')" />
        </el-form-item>
        <el-form-item label="Api-Key">
          <el-input
            v-model="form.apiKey"
            size="large"
            type="password"
            show-password
            :placeholder="t('apiKeyPlaceholder')"
            @keyup.enter="submit"
          />
        </el-form-item>
        <el-button class="login-button" type="primary" size="large" :loading="loading" @click="submit">
          <LogIn :size="18" />
          {{ t('enterCockpit') }}
        </el-button>
      </el-form>

      <p class="login-note">{{ t('loginNote') }}</p>
    </section>
  </main>
</template>
