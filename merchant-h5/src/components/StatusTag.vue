<script setup lang="ts">
import { computed } from 'vue'

import { useI18n } from '../i18n'

const props = defineProps<{
  status?: string | null
  label?: string | null
}>()

const { statusText } = useI18n()

const tagType = computed(() => {
  switch (props.status) {
    case 'success':
    case 'imported':
      return 'success'
    case 'failed':
      return 'danger'
    case 'partial':
      return 'warning'
    case 'pending':
    case 'running':
      return 'primary'
    case 'skipped':
      return 'info'
    default:
      return 'info'
  }
})
</script>

<template>
  <el-tag :type="tagType" effect="light" round>
    {{ statusText(status, label) }}
  </el-tag>
</template>
