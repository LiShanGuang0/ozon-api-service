<script setup lang="ts">
import { onMounted, reactive, ref, watch } from 'vue'
import { Search } from 'lucide-vue-next'

import { getProducts, type ProductItem } from '../api/merchant'
import { useI18n } from '../i18n'
import StatusTag from '../components/StatusTag.vue'
import { useDynamicTranslations } from '../composables/useDynamicTranslations'

const { t } = useI18n()
const { locale, ensureTranslations, translatedText } = useDynamicTranslations()
const loading = ref(false)
const products = ref<ProductItem[]>([])
const total = ref(0)
const query = reactive({
  page: 1,
  size: 20,
  keyword: '',
  status: '',
})

async function load() {
  loading.value = true
  try {
    const result = await getProducts(query)
    products.value = result.items
    total.value = result.total
    void ensureProductTranslations()
  } finally {
    loading.value = false
  }
}

function ensureProductTranslations() {
  return ensureTranslations(products.value.map((product) => product.name))
}

function search() {
  query.page = 1
  load()
}

onMounted(load)

watch(locale, () => {
  void ensureProductTranslations()
})
</script>

<template>
  <section class="content-panel">
    <header class="toolbar">
      <div>
        <h2>{{ t('productListTitle') }}</h2>
        <p>{{ t('productListDesc') }}</p>
      </div>
      <div class="toolbar-actions">
        <el-input v-model="query.keyword" clearable :placeholder="t('searchProduct')" size="large" @keyup.enter="search">
          <template #prefix>
            <Search :size="16" />
          </template>
        </el-input>
        <el-select v-model="query.status" clearable :placeholder="t('status')" size="large" @change="search">
          <el-option :label="t('pending')" value="pending" />
          <el-option :label="t('imported')" value="imported" />
          <el-option :label="t('failed')" value="failed" />
          <el-option :label="t('skipped')" value="skipped" />
        </el-select>
        <el-button type="primary" size="large" @click="search">{{ t('query') }}</el-button>
      </div>
    </header>

    <el-table v-loading="loading" :data="products" class="data-table" row-key="id">
      <el-table-column prop="offer_id" :label="t('offerId')" min-width="150" fixed />
      <el-table-column :label="t('productImage')" width="96">
        <template #default="{ row }">
          <el-image
            v-if="row.cover_image_url"
            class="product-thumb"
            :src="row.cover_image_url"
            fit="cover"
            lazy
            :preview-src-list="[row.cover_image_url]"
            preview-teleported
          />
          <span v-else class="image-placeholder">-</span>
        </template>
      </el-table-column>
      <el-table-column :label="t('productName')" min-width="220" show-overflow-tooltip>
        <template #default="{ row }">
          {{ translatedText(row.name) || '-' }}
        </template>
      </el-table-column>
      <el-table-column prop="product_id" :label="t('ozonProductId')" width="150" />
      <el-table-column prop="sku" label="SKU" width="130" />
      <el-table-column prop="price" :label="t('price')" width="110" />
      <el-table-column :label="t('inventoryInfo')" min-width="190">
        <template #default="{ row }">
          <div class="inventory-cell">
            <span>{{ t('warehouseName') }}：{{ row.warehouse_name || '-' }}</span>
            <strong>{{ t('stockQty') }}：{{ row.stock ?? '-' }}</strong>
          </div>
        </template>
      </el-table-column>
      <el-table-column :label="t('status')" width="160">
        <template #default="{ row }">
          <StatusTag :status="row.sync_status" :label="row.sync_status_label" />
        </template>
      </el-table-column>
      <el-table-column prop="last_task_id" :label="t('lastTask')" width="130" />
      <el-table-column prop="updated_at" :label="t('updatedAt')" min-width="170" />
    </el-table>

    <footer class="table-footer">
      <el-pagination
        v-model:current-page="query.page"
        v-model:page-size="query.size"
        background
        layout="total, sizes, prev, pager, next"
        :total="total"
        @change="load"
      />
    </footer>
  </section>
</template>
