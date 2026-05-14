<script setup lang="ts">
import { computed, onMounted, reactive, ref } from 'vue'
import { Copy, KeyRound, RefreshCw, ShieldCheck } from 'lucide-vue-next'
import { ElMessage } from 'element-plus'

import {
  createActivationCode,
  listActivationCodes,
  type AppActivationCodeCreateResult,
  type AppActivationCodeItem,
} from '../api/merchant'

const ADMIN_TOKEN_KEY = 'ozon-activation-admin-token'
const loading = ref(false)
const listLoading = ref(false)
const result = ref<AppActivationCodeCreateResult | null>(null)
const activations = ref<AppActivationCodeItem[]>([])

const form = reactive({
  adminToken: sessionStorage.getItem(ADMIN_TOKEN_KEY) || '',
  deviceId: '',
  macAddress: '',
  clientId: '',
  apiKey: '',
  activationCode: '',
  validDays: 365,
})

const canSubmit = computed(() =>
  Boolean(form.adminToken.trim() && form.deviceId.trim() && form.clientId.trim() && form.apiKey.trim() && form.validDays),
)

onMounted(() => {
  if (form.adminToken.trim()) {
    void loadActivations()
  }
})

async function submit() {
  if (!canSubmit.value) {
    ElMessage.warning('请填写管理员 Token、设备 ID、Client-Id、Api-Key 和有效天数')
    return
  }

  loading.value = true
  try {
    const data = await createActivationCode(
      {
        device_id: form.deviceId.trim(),
        mac_address: form.macAddress.trim() || null,
        client_id: form.clientId.trim(),
        api_key: form.apiKey.trim(),
        activation_code: form.activationCode.trim() || null,
        valid_days: form.validDays,
      },
      form.adminToken.trim(),
    )
    sessionStorage.setItem(ADMIN_TOKEN_KEY, form.adminToken.trim())
    result.value = data
    form.apiKey = ''
    form.activationCode = ''
    ElMessage.success('激活码已生成')
    await loadActivations()
  } finally {
    loading.value = false
  }
}

async function loadActivations() {
  if (!form.adminToken.trim()) {
    ElMessage.warning('请先填写管理员 Token')
    return
  }

  listLoading.value = true
  try {
    sessionStorage.setItem(ADMIN_TOKEN_KEY, form.adminToken.trim())
    const data = await listActivationCodes(form.adminToken.trim())
    activations.value = data.items
  } finally {
    listLoading.value = false
  }
}

async function copyActivationCode(code?: string | null) {
  if (!code) {
    ElMessage.warning('该记录没有可复制的激活码，可能是旧版本 hash-only 记录')
    return
  }
  await navigator.clipboard.writeText(code)
  ElMessage.success('激活码已复制')
}

function statusText(status: string) {
  const map: Record<string, string> = {
    pending: '待激活',
    active: '已绑定',
    revoked: '已撤销',
  }
  return map[status] || status
}

function formatTime(value?: string | null) {
  if (!value) return '-'
  return value.replace('T', ' ').slice(0, 19)
}
</script>

<template>
  <main class="activation-admin-page">
    <section class="activation-admin-card">
      <div class="login-brand">
        <div class="brand-mark">
          <KeyRound :size="24" />
        </div>
        <div>
          <strong>App 激活管理</strong>
          <span>查看历史记录并为 Android 平板新增激活码</span>
        </div>
      </div>

      <div class="login-title">
        <span>
          <ShieldCheck :size="16" />
          激活码管理
        </span>
        <h1>激活码列表与新增</h1>
        <p>输入管理员 Token 后可查看历史激活码，也可以为指定设备新增或重置激活码。Api-Key 只保存指纹。</p>
      </div>

      <el-form label-position="top" @submit.prevent="submit">
        <el-form-item label="管理员 Token">
          <div class="activation-token-row">
            <el-input
              v-model="form.adminToken"
              size="large"
              type="password"
              show-password
              placeholder="请输入 APP_ACTIVATION_ADMIN_TOKEN"
            />
            <el-button size="large" :loading="listLoading" @click="loadActivations">
              <RefreshCw :size="16" />
              刷新列表
            </el-button>
          </div>
        </el-form-item>

        <div class="activation-admin-grid">
          <el-form-item label="设备 ID">
            <el-input v-model="form.deviceId" size="large" placeholder="从 App 激活页复制设备 ID" />
          </el-form-item>
          <el-form-item label="MAC 地址（可选）">
            <el-input v-model="form.macAddress" size="large" placeholder="可不填" />
          </el-form-item>
        </div>

        <div class="activation-admin-grid">
          <el-form-item label="Client-Id">
            <el-input v-model="form.clientId" size="large" placeholder="请输入 Ozon Client-Id" />
          </el-form-item>
          <el-form-item label="有效天数">
            <el-input-number v-model="form.validDays" size="large" :min="1" :max="3650" controls-position="right" />
          </el-form-item>
        </div>

        <el-form-item label="Api-Key">
          <el-input v-model="form.apiKey" size="large" type="password" show-password placeholder="请输入 Ozon Api-Key" />
        </el-form-item>

        <el-form-item label="自定义激活码（可选）">
          <el-input v-model="form.activationCode" size="large" placeholder="不填则后端自动生成" @keyup.enter="submit" />
        </el-form-item>

        <el-button class="login-button" type="primary" size="large" :loading="loading" @click="submit">
          生成激活码
        </el-button>
      </el-form>

      <div v-if="result" class="activation-result">
        <span>激活码</span>
        <div class="activation-code-row">
          <strong>{{ result.activation_code }}</strong>
          <el-button type="primary" plain @click="copyActivationCode(result.activation_code)">
            <Copy :size="16" />
            复制
          </el-button>
        </div>
        <p>设备 ID：{{ result.device_id }}</p>
        <p>Client-Id：{{ result.client_id }}</p>
        <p>有效期至：{{ result.expires_at }}</p>
      </div>

      <section class="activation-list-panel">
        <div class="activation-list-header">
          <div>
            <h2>历史激活码</h2>
            <p>共 {{ activations.length }} 条记录</p>
          </div>
          <el-button :loading="listLoading" @click="loadActivations">
            <RefreshCw :size="16" />
            刷新
          </el-button>
        </div>

        <el-table v-loading="listLoading" :data="activations" border empty-text="暂无激活码记录">
          <el-table-column label="激活码" min-width="180">
            <template #default="{ row }">
              <div class="activation-table-code">
                <strong>{{ row.activation_code || '旧记录不可查看' }}</strong>
                <el-button link type="primary" @click="copyActivationCode(row.activation_code)">
                  复制
                </el-button>
              </div>
            </template>
          </el-table-column>
          <el-table-column prop="status" label="状态" width="100">
            <template #default="{ row }">
              <el-tag :type="row.status === 'active' ? 'success' : row.status === 'revoked' ? 'danger' : 'warning'">
                {{ statusText(row.status) }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="client_id" label="Client-Id" min-width="130" />
          <el-table-column prop="device_id" label="设备 ID" min-width="220" show-overflow-tooltip />
          <el-table-column prop="mac_address" label="MAC" min-width="130" show-overflow-tooltip />
          <el-table-column label="有效期" min-width="160">
            <template #default="{ row }">{{ formatTime(row.expires_at) }}</template>
          </el-table-column>
          <el-table-column label="激活时间" min-width="160">
            <template #default="{ row }">{{ formatTime(row.activated_at) }}</template>
          </el-table-column>
          <el-table-column label="最近访问" min-width="160">
            <template #default="{ row }">{{ formatTime(row.last_seen_at) }}</template>
          </el-table-column>
        </el-table>
      </section>
    </section>
  </main>
</template>
