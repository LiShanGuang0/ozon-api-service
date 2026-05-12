<script setup lang="ts">
import { computed, onMounted, onUnmounted, ref, watch } from 'vue'
import { CirclePause, CirclePlay, Radio, RotateCw } from 'lucide-vue-next'

import { getTaskEvents, type TaskEvent } from '../api/merchant'
import { useI18n } from '../i18n'
import { useDynamicTranslations } from '../composables/useDynamicTranslations'

interface CompletionProduct {
  offer_id?: string | null
  name?: string | null
  product_id?: number | string | null
  sku?: number | string | null
  price?: number | string | null
  currency_code?: string | null
  cover_image_url?: string | null
  warehouse_name?: string | null
  requested_stock?: number | string | null
  stock?: number | string | null
  present?: number | string | null
  reserved?: number | string | null
}

const props = withDefaults(
  defineProps<{
    embedded?: boolean
    limit?: number
  }>(),
  {
    embedded: false,
    limit: 30,
  },
)

const loading = ref(false)
const paused = ref(false)
const events = ref<TaskEvent[]>([])
const todayCount = ref(0)
const { t } = useI18n()
const { locale, ensureTranslations, translatedText } = useDynamicTranslations()
let timer: number | undefined

const emptyText = computed(() => (loading.value ? t('readingConsole') : t('emptyConsole')))

async function loadEvents() {
  if (paused.value) return
  loading.value = true
  try {
    const result = await getTaskEvents({ limit: props.limit })
    events.value = result.items
    todayCount.value = result.today_count
    void ensureErrorTranslations()
  } finally {
    loading.value = false
  }
}

function ensureErrorTranslations() {
  return ensureTranslations(
    events.value.flatMap((event) => [
      event.message,
      event.error_message,
      ...completionProducts(event).map((product) => product.name),
    ]),
  )
}

function togglePause() {
  paused.value = !paused.value
}

function statusCode(status: string) {
  if (status === 'success' || status === 'imported') return 'DONE'
  if (status === 'failed') return 'FAIL'
  if (status === 'skipped') return 'SKIP'
  return 'WAIT'
}

function eventMeta(event: TaskEvent) {
  const parts = []
  if (event.offer_id) parts.push(`offer=${event.offer_id}`)
  if (event.ozon_task_id) parts.push(`task=${event.ozon_task_id}`)
  if (event.product_id) parts.push(`product=${event.product_id}`)
  if (event.sku) parts.push(`sku=${event.sku}`)
  return parts.join(' ')
}

function completionProducts(event: TaskEvent): CompletionProduct[] {
  if (event.event_type !== 'product_import_completion') return []
  if (!event.payload || typeof event.payload !== 'object') return []
  const products = (event.payload as { products?: unknown }).products
  return Array.isArray(products) ? (products as CompletionProduct[]) : []
}

function productStock(product: CompletionProduct) {
  return product.present ?? product.stock ?? product.requested_stock ?? '-'
}

onMounted(() => {
  loadEvents()
  timer = window.setInterval(loadEvents, 5000)
})

onUnmounted(() => {
  if (timer) window.clearInterval(timer)
})

watch(locale, () => {
  void ensureErrorTranslations()
})
</script>

<template>
  <section class="task-stream" :class="{ embedded }">
    <header class="panel-header">
      <div>
        <h2>{{ t('terminalConsole') }}</h2>
        <p>
          <Radio :size="14" />
          {{ paused ? t('paused') : t('refreshing') }}
          <span>{{ t('todayCount', { count: todayCount }) }}</span>
        </p>
      </div>
      <div class="panel-actions">
        <el-button circle @click="loadEvents">
          <RotateCw :size="16" />
        </el-button>
        <el-button circle @click="togglePause">
          <CirclePlay v-if="paused" :size="16" />
          <CirclePause v-else :size="16" />
        </el-button>
      </div>
    </header>

    <div v-if="events.length" class="stream-list console-list">
      <article v-for="event in events" :key="event.id" class="stream-item console-line" :class="`event-${event.status}`">
        <time>{{ new Date(event.created_at).toLocaleTimeString('zh-CN', { hour12: false }) }}</time>
        <span class="console-code">{{ statusCode(event.status) }}</span>
        <div class="stream-body">
          <p>
            <span class="console-prompt">$</span>
            {{ translatedText(event.message) }}
            <small v-if="eventMeta(event)" class="console-meta">{{ eventMeta(event) }}</small>
          </p>
          <div v-if="completionProducts(event).length" class="completion-card-list">
            <article
              v-for="product in completionProducts(event)"
              :key="String(product.offer_id || product.product_id || product.sku)"
              class="completion-card"
            >
              <el-image
                v-if="product.cover_image_url"
                class="completion-thumb"
                :src="product.cover_image_url"
                fit="cover"
                lazy
                preview-teleported
                :preview-src-list="[product.cover_image_url]"
              />
              <span v-else class="completion-thumb placeholder">-</span>
              <div class="completion-info">
                <strong>{{ translatedText(product.name) || product.offer_id || '-' }}</strong>
                <span>offer={{ product.offer_id || '-' }} · SKU={{ product.sku || '-' }}</span>
                <span>{{ t('warehouseName') }}：{{ product.warehouse_name || '-' }}</span>
              </div>
              <div class="completion-stock">
                <span>{{ t('stockQty') }}</span>
                <strong>{{ productStock(product) }}</strong>
                <small>{{ t('reservedStock') }}：{{ product.reserved ?? '-' }}</small>
              </div>
            </article>
          </div>
          <small v-if="event.error_message">{{ translatedText(event.error_message) }}</small>
        </div>
      </article>
    </div>

    <el-empty v-else :description="emptyText" :image-size="90" />
  </section>
</template>
