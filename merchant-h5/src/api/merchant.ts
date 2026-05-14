import { http } from './http'

export interface PageResult<T> {
  total: number
  page: number
  size: number
  items: T[]
}

export interface MerchantProfile {
  merchant_id: string | null
  client_id: string
  shop_name: string | null
  display_name: string | null
  logo_url: string | null
  status: string
  currency_code: string | null
  default_warehouse_id: number | null
  contact_name: string | null
  contact_phone: string | null
  contact_email: string | null
  last_connected_at: string | null
  last_error: string | null
}

export interface AppActivationCheckResult {
  bound: boolean
  expired: boolean
  activation_required: boolean
  status: string | null
  reason: string | null
  client_id: string | null
  expires_at: string | null
}

export interface AppActivationBindResult {
  bound: boolean
  client_id: string
  expires_at: string
  profile: MerchantProfile
}

export interface AppActivationCodeCreateResult {
  device_id: string
  client_id: string
  activation_code: string
  expires_at: string
  status: string
}

export interface AppActivationCodeItem {
  id: number
  device_id: string
  mac_address: string | null
  client_id: string
  activation_code: string | null
  status: string
  expires_at: string
  activated_at: string | null
  last_seen_at: string | null
  created_at: string
  updated_at: string
}

export interface AppActivationCodeListResult {
  items: AppActivationCodeItem[]
}

export interface DashboardMetric {
  key: string
  label: string
  value: number
}

export interface TaskEvent {
  id: number
  event_type: string
  status: string
  status_label: string
  offer_id: string | null
  product_id: number | null
  sku: number | null
  ozon_task_id: number | null
  request_id: string | null
  message: string
  error_message: string | null
  payload: unknown
  created_at: string
}

export interface DashboardData {
  profile: MerchantProfile
  metrics: DashboardMetric[]
  task_status_counts: Record<string, number>
  product_status_counts: Record<string, number>
  today_event_count: number
  recent_events: TaskEvent[]
}

export interface ProductItem {
  id: number
  offer_id: string
  local_sku: string | null
  name: string | null
  product_id: number | null
  sku: number | null
  currency_code: string | null
  price: string | number | null
  old_price: string | number | null
  warehouse_id: number | null
  warehouse_name: string | null
  stock: number | null
  cover_image_url: string | null
  sync_status: string
  sync_status_label: string
  ozon_status: string | null
  last_task_id: number | null
  last_error: unknown
  updated_at: string | null
  created_at: string | null
}

export interface TaskEventsResult {
  items: TaskEvent[]
  next_before_id: number | null
  today_count: number
}

export interface TranslateTextItem {
  text: string
  translated_text: string
  source_language: string | null
  target_language: 'zh' | 'ru' | 'en'
  translated: boolean
  error?: string | null
}

export interface TranslateTextResult {
  items: TranslateTextItem[]
}

export function bootstrapMerchant(payload: { client_id: string; api_key: string }) {
  return http.post<unknown, { profile: MerchantProfile; initialized_from_ozon: boolean; credential_valid: boolean }>(
    '/merchant/bootstrap',
    payload,
  )
}

export function checkActivation(payload: { device_id: string; mac_address?: string | null }) {
  return http.post<unknown, AppActivationCheckResult>('/app-activations/check', payload)
}

export function bindActivation(payload: {
  device_id: string
  mac_address?: string | null
  client_id: string
  api_key: string
  activation_code: string
}) {
  return http.post<unknown, AppActivationBindResult>('/app-activations/bind', payload)
}

export function createActivationCode(
  payload: {
    device_id: string
    mac_address?: string | null
    client_id: string
    api_key: string
    activation_code?: string | null
    valid_days?: number
    expires_at?: string | null
  },
  adminToken: string,
) {
  return http.post<unknown, AppActivationCodeCreateResult>('/app-activations/codes', payload, {
    headers: {
      'X-Admin-Token': adminToken,
    },
  })
}

export function listActivationCodes(adminToken: string) {
  return http.get<unknown, AppActivationCodeListResult>('/app-activations/codes', {
    headers: {
      'X-Admin-Token': adminToken,
    },
  })
}

export function getDashboard() {
  return http.get<unknown, DashboardData>('/merchant/dashboard')
}

export function getProfile() {
  return http.get<unknown, MerchantProfile>('/merchant/profile')
}

export function getProducts(params: Record<string, unknown>) {
  return http.get<unknown, PageResult<ProductItem>>('/merchant/products', { params })
}

export function getTaskEvents(params: Record<string, unknown>) {
  return http.get<unknown, TaskEventsResult>('/merchant/task-events', { params })
}

export function translateTexts(payload: {
  texts: string[]
  target_language: 'zh' | 'ru' | 'en'
  source_language?: string
}) {
  return http.post<unknown, TranslateTextResult>('/merchant/translate', payload)
}
