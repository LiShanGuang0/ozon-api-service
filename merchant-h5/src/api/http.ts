import axios from 'axios'
import { ElMessage } from 'element-plus'

import { useMerchantStore } from '../stores/merchant'

export interface ApiEnvelope<T> {
  code: number
  msg: string
  data: T
}

const apiBaseURL = import.meta.env.VITE_API_BASE_URL || '/api'

export const http = axios.create({
  baseURL: apiBaseURL,
  timeout: 20000,
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
    ElMessage.error(message)
    return Promise.reject(error)
  },
)
