<script setup lang="ts">
import { onMounted, reactive, ref } from 'vue'
import { getPushTaskDetail, getPushTasks, type PushTask, type PushTaskDetail } from '../api/merchant'
import { useI18n } from '../i18n'
import StatusTag from '../components/StatusTag.vue'
import TaskStreamPanel from '../components/TaskStreamPanel.vue'

const { t, messageText } = useI18n()
const loading = ref(false)
const tasks = ref<PushTask[]>([])
const total = ref(0)
const detailVisible = ref(false)
const detailLoading = ref(false)
const detail = ref<PushTaskDetail | null>(null)
const query = reactive({
  page: 1,
  size: 20,
  status: '',
})

async function load() {
  loading.value = true
  try {
    const result = await getPushTasks(query)
    tasks.value = result.items
    total.value = result.total
  } finally {
    loading.value = false
  }
}

async function openDetail(taskId: number) {
  detailVisible.value = true
  detailLoading.value = true
  try {
    detail.value = await getPushTaskDetail(taskId)
  } finally {
    detailLoading.value = false
  }
}

function search() {
  query.page = 1
  load()
}

onMounted(load)
</script>

<template>
  <div class="tasks-layout">
    <section class="content-panel">
      <header class="toolbar">
        <div>
          <h2>{{ t('pushTasks') }}</h2>
          <p>{{ t('pushTasksDesc') }}</p>
        </div>
        <div class="toolbar-actions compact">
          <el-select v-model="query.status" clearable :placeholder="t('taskStatus')" size="large" @change="search">
            <el-option :label="t('pending')" value="pending" />
            <el-option :label="t('imported')" value="imported" />
            <el-option :label="t('failed')" value="failed" />
            <el-option :label="t('partialSuccess')" value="partial" />
            <el-option :label="t('skipped')" value="skipped" />
          </el-select>
          <el-button type="primary" size="large" @click="search">{{ t('query') }}</el-button>
        </div>
      </header>

      <el-table v-loading="loading" :data="tasks" class="data-table" row-key="id">
        <el-table-column prop="task_id" :label="t('taskId')" width="130" fixed />
        <el-table-column :label="t('status')" width="160">
          <template #default="{ row }">
            <StatusTag :status="row.status" :label="row.status_label" />
          </template>
        </el-table-column>
        <el-table-column prop="total_count" :label="t('productCount')" width="110" />
        <el-table-column prop="success_count" :label="t('success')" width="100" />
        <el-table-column prop="failed_count" :label="t('failed')" width="100" />
        <el-table-column prop="submitted_at" :label="t('submittedAt')" min-width="170" />
        <el-table-column :label="t('action')" width="110" fixed="right">
          <template #default="{ row }">
            <el-button type="primary" link @click="openDetail(row.task_id)">{{ t('view') }}</el-button>
          </template>
        </el-table-column>
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

    <TaskStreamPanel embedded :limit="20" />
  </div>

  <el-drawer v-model="detailVisible" :title="t('taskDetail')" size="58%">
    <div v-loading="detailLoading">
      <el-descriptions v-if="detail" :column="2" border>
        <el-descriptions-item :label="t('taskId')">{{ detail.task.task_id }}</el-descriptions-item>
        <el-descriptions-item :label="t('status')">
          <StatusTag :status="String(detail.task.status)" :label="String(detail.task.status_label || detail.task.status)" />
        </el-descriptions-item>
        <el-descriptions-item :label="t('submittedAt')">{{ detail.task.submitted_at }}</el-descriptions-item>
        <el-descriptions-item :label="t('finishedAt')">{{ detail.task.finished_at || '-' }}</el-descriptions-item>
      </el-descriptions>

      <el-table v-if="detail" :data="detail.items" class="drawer-table">
        <el-table-column prop="offer_id" :label="t('offerId')" min-width="150" />
        <el-table-column prop="product_id" :label="t('ozonProductId')" width="150" />
        <el-table-column :label="t('status')" width="160">
          <template #default="{ row }">
            <StatusTag :status="String(row.status)" :label="String(row.status_label || row.status)" />
          </template>
        </el-table-column>
        <el-table-column :label="t('errorInfo')" min-width="220" show-overflow-tooltip>
          <template #default="{ row }">{{ messageText(String(row.errors || '')) }}</template>
        </el-table-column>
      </el-table>
    </div>
  </el-drawer>
</template>
