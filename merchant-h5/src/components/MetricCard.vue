<script setup lang="ts">
import { computed } from 'vue'
import type { Component } from 'vue'

const props = defineProps<{
  label: string
  value: number
  tone?: 'blue' | 'green' | 'red' | 'orange'
  icon: Component
}>()

const toneClass = computed(() => `metric-${props.tone || 'blue'}`)
</script>

<template>
  <section class="metric-card" :class="toneClass">
    <div class="metric-icon">
      <component :is="icon" :size="22" />
    </div>
    <div>
      <span>{{ label }}</span>
      <strong>{{ value }}</strong>
    </div>
  </section>
</template>
