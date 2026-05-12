<script setup lang="ts">
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ArrowLeft, Box, Home, LogOut } from 'lucide-vue-next'
import zhCn from 'element-plus/es/locale/lang/zh-cn'
import en from 'element-plus/es/locale/lang/en'
import ru from 'element-plus/es/locale/lang/ru'

import { useI18n, type Locale } from './i18n'
import { useMerchantStore } from './stores/merchant'

const route = useRoute()
const router = useRouter()
const merchant = useMerchantStore()
const { locale, setLocale, t } = useI18n()
const currentLocale = computed({
  get: () => locale.value,
  set: (value: Locale) => setLocale(value),
})
const elementLocale = computed(() => {
  if (locale.value === 'ru') return ru
  if (locale.value === 'en') return en
  return zhCn
})

const pageTitle = computed(() => t(String(route.meta.titleKey || 'workspace')))
const isCockpit = computed(() => route.path === '/dashboard')
const isLogin = computed(() => route.path === '/login')

function goHome() {
  router.push('/dashboard')
}

function logout() {
  merchant.logout()
  router.push('/login')
}

</script>

<template>
  <el-config-provider :locale="elementLocale">
  <div class="app-shell cockpit-shell" :class="{ 'login-shell': isLogin }">
    <RouterView v-if="isLogin" />
    <main v-if="!isLogin" class="main-area">
      <header v-if="!isLogin" class="topbar cockpit-topbar">
        <div class="brand compact-brand">
        <div class="brand-mark">
          <Box :size="22" />
        </div>
        <div>
          <strong>{{ t('appName') }}</strong>
          <span>{{ t('merchantConsole') }}</span>
        </div>
      </div>

        <div class="page-heading">
          <el-button v-if="!isCockpit" circle size="large" @click="goHome">
            <ArrowLeft :size="18" />
          </el-button>
          <el-button v-if="!isCockpit" circle size="large" @click="goHome">
            <Home :size="18" />
          </el-button>
          <div>
          <h1>{{ pageTitle }}</h1>
            <p>{{ isCockpit ? t('cockpitTitle') : t('detailSubtitle') }}</p>
          </div>
        </div>

        <div class="client-box">
          <el-segmented
            v-model="currentLocale"
            :options="[
              { label: '中', value: 'zh' },
              { label: 'RU', value: 'ru' },
              { label: 'EN', value: 'en' },
            ]"
          />
          <el-button size="large" @click="logout">
            <LogOut :size="16" />
            {{ t('switchAccount') }}
          </el-button>
        </div>
      </header>

      <RouterView v-if="!isLogin" />
    </main>
  </div>
  </el-config-provider>
</template>
