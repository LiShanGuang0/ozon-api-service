<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import {
  AlertCircle,
  ArrowRight,
  CheckCircle2,
  ClipboardList,
  Clock3,
  PackageSearch,
  Send,
  Store,
} from 'lucide-vue-next'

import { getDashboard, type DashboardData } from '../api/merchant'
import { useI18n } from '../i18n'
import MetricCard from '../components/MetricCard.vue'
import TaskStreamPanel from '../components/TaskStreamPanel.vue'
import StatusTag from '../components/StatusTag.vue'

const router = useRouter()
const { t, statusText } = useI18n()
const loading = ref(false)
const data = ref<DashboardData | null>(null)

const metricIcons = [Send, CheckCircle2, AlertCircle, Clock3]
const metricTones = ['blue', 'green', 'red', 'orange'] as const
const featureCards = [
  {
    titleKey: 'pushTasks',
    descKey: 'pushTasksDesc',
    path: '/push-tasks',
    icon: ClipboardList,
    tone: 'blue',
  },
  {
    titleKey: 'products',
    descKey: 'productsDesc',
    path: '/products',
    icon: PackageSearch,
    tone: 'green',
  },
  {
    titleKey: 'merchantInfo',
    descKey: 'merchantInfoDesc',
    path: '/merchant',
    icon: Store,
    tone: 'orange',
  },
]

async function load() {
  loading.value = true
  try {
    data.value = await getDashboard()
  } finally {
    loading.value = false
  }
}

onMounted(load)
</script>

<template>
  <div v-loading="loading" class="cockpit-dashboard">
    <section class="cockpit-hero">
      <div class="hero-copy">
        <span class="hero-kicker">OZON MERCHANT COCKPIT</span>
        <h2>{{ data?.profile.display_name || data?.profile.shop_name || t('cockpitTitle') }}</h2>
        <p>{{ t('cockpitSubtitle') }}</p>
      </div>

      <div class="hero-status">
        <span>{{ t('currentStatus') }}</span>
        <StatusTag :status="data?.profile.status" :label="data?.profile.status === 'active' ? t('connected') : statusText(data?.profile.status)" />
      </div>
    </section>

    <section class="cockpit-main">
      <div class="cockpit-left">
      <div class="metrics-grid">
        <MetricCard
          v-for="(metric, index) in data?.metrics || []"
          :key="metric.key"
          :label="t(metric.key)"
          :value="metric.value"
          :tone="metricTones[index] || 'blue'"
          :icon="metricIcons[index] || Send"
        />
      </div>

        <section class="feature-grid">
          <button
            v-for="item in featureCards"
            :key="item.path"
            class="feature-card"
            :class="`feature-${item.tone}`"
            type="button"
            @click="router.push(item.path)"
          >
            <span class="feature-icon">
              <component :is="item.icon" :size="24" />
            </span>
            <span class="feature-body">
              <strong>{{ t(item.titleKey) }}</strong>
              <small>{{ t(item.descKey) }}</small>
            </span>
            <ArrowRight :size="20" />
          </button>
        </section>

      <section class="content-panel">
        <header class="panel-header">
          <div>
            <h2>{{ t('productStatus') }}</h2>
            <p>{{ t('productStatusDesc') }}</p>
          </div>
        </header>
        <div class="status-grid">
          <div v-for="(count, status) in data?.product_status_counts" :key="status" class="status-stat">
            <span>{{ statusText(String(status)) }}</span>
            <strong>{{ count }}</strong>
          </div>
        </div>
      </section>
      </div>

      <TaskStreamPanel embedded :limit="36" />
    </section>
  </div>
</template>
