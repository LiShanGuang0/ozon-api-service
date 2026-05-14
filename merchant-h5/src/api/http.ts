import axios, { type AxiosAdapter, type AxiosRequestHeaders } from 'axios'
import { Capacitor, CapacitorHttp } from '@capacitor/core'
import { ElMessage } from 'element-plus'

import { useMerchantStore } from '../stores/merchant'

export interface ApiEnvelope<T> {
  code: number
  msg: string
  data: T
}

const apiBaseURL = import.meta.env.VITE_API_BASE_URL || '/api'

function normalizeHeaders(headers: unknown): Record<string, string> {
  const source =
    headers && typeof headers === 'object' && 'toJSON' in headers && typeof headers.toJSON === 'function'
      ? headers.toJSON()
      : headers
  const normalized: Record<string, string> = {}

  Object.entries((source || {}) as AxiosRequestHeaders).forEach(([key, value]) => {
    if (value === undefined || value === null || value === false) return
    normalized[key] = String(value)
  })

  return normalized
}

const nativeHttpAdapter: AxiosAdapter = async (config) => {
  const url = axios.getUri(config)
  try {
    const response = await CapacitorHttp.request({
      url,
      method: (config.method || 'get').toUpperCase(),
      headers: normalizeHeaders(config.headers),
      data: config.data,
      responseType: 'text',
      connectTimeout: config.timeout,
      readTimeout: config.timeout,
    })

    return {
      data: response.data,
      status: response.status,
      statusText: String(response.status),
      headers: response.headers,
      config,
      request: null,
    }
  } catch (error) {
    const message = error instanceof Error ? error.message : JSON.stringify(error)
    throw new Error(`Native HTTP failed: ${message}`)
  }
}

export const http = axios.create({
  baseURL: apiBaseURL,
  timeout: 20000,
  adapter: Capacitor.isNativePlatform() ? nativeHttpAdapter : undefined,
})

http.interceptors.request.use((config) => {
  const merchant = useMerchantStore()
  if (merchant.clientId) {
    config.headers['X-Merchant-Client-Id'] = merchant.clientId
    config.headers['Client-Id'] = merchant.clientId
  }
  if (merchant.apiKey) {
    config.headers['Api-Key'] = merchant.apiKey
  }
  return config
})

http.interceptors.response.use(
  (response) => {
    const payload = response.data as ApiEnvelope<unknown>
    if (payload && typeof payload === 'object' && 'code' in payload && 'data' in payload) {
      if (payload.code >= 200 && payload.code < 300) {
        return payload.data
      }
      throw new Error(payload.msg || '请求失败')
    }
    return response.data
  },
  (error) => {
    const message = error?.response?.data?.msg || error?.message || '网络请求失败'
    console.error('HTTP request failed', error)
    ElMessage.error(message)
    return Promise.reject(error)
  },
)
