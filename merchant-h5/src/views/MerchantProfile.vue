<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { getProfile, type MerchantProfile } from '../api/merchant'
import { useI18n } from '../i18n'
import StatusTag from '../components/StatusTag.vue'

const { t, statusText } = useI18n()
const loading = ref(false)
const profile = ref<MerchantProfile | null>(null)

async function load() {
  loading.value = true
  try {
    profile.value = await getProfile()
  } finally {
    loading.value = false
  }
}

onMounted(load)
</script>

<template>
  <section v-loading="loading" class="content-panel profile-page">
    <header class="panel-header">
      <div>
        <h2>{{ t('merchantInfo') }}</h2>
        <p>{{ t('merchantInfoPageDesc') }}</p>
      </div>
      <StatusTag :status="profile?.status" :label="profile?.status === 'active' ? statusText('active') : statusText(profile?.status)" />
    </header>

    <el-descriptions v-if="profile" :column="2" border>
      <el-descriptions-item :label="t('merchantId')">{{ profile.merchant_id || '-' }}</el-descriptions-item>
      <el-descriptions-item label="Client-Id">{{ profile.client_id }}</el-descriptions-item>
      <el-descriptions-item :label="t('shopName')">{{ profile.display_name || profile.shop_name || '-' }}</el-descriptions-item>
      <el-descriptions-item :label="t('currency')">{{ profile.currency_code || '-' }}</el-descriptions-item>
      <el-descriptions-item :label="t('defaultWarehouse')">{{ profile.default_warehouse_id || '-' }}</el-descriptions-item>
      <el-descriptions-item :label="t('contactName')">{{ profile.contact_name || '-' }}</el-descriptions-item>
      <el-descriptions-item :label="t('contactPhone')">{{ profile.contact_phone || '-' }}</el-descriptions-item>
      <el-descriptions-item :label="t('contactEmail')">{{ profile.contact_email || '-' }}</el-descriptions-item>
      <el-descriptions-item :label="t('lastConnected')">{{ profile.last_connected_at || '-' }}</el-descriptions-item>
      <el-descriptions-item :label="t('lastError')">{{ profile.last_error || '-' }}</el-descriptions-item>
    </el-descriptions>
  </section>
</template>
