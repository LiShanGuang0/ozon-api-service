import { defineStore } from 'pinia'

const CLIENT_ID_KEY = 'ozon-merchant-client-id'
const API_KEY_KEY = 'ozon-merchant-api-key'

export const useMerchantStore = defineStore('merchant', {
  state: () => ({
    clientId: localStorage.getItem(CLIENT_ID_KEY) || '',
    apiKey: sessionStorage.getItem(API_KEY_KEY) || '',
  }),
  getters: {
    isReady: (state) => Boolean(state.clientId && state.apiKey),
  },
  actions: {
    setCredentials(clientId: string, apiKey: string) {
      this.clientId = clientId.trim()
      this.apiKey = apiKey.trim()
      if (this.clientId) {
        localStorage.setItem(CLIENT_ID_KEY, this.clientId)
      }
      if (this.apiKey) {
        sessionStorage.setItem(API_KEY_KEY, this.apiKey)
      }
    },
    setClientId(value: string) {
      this.clientId = value.trim()
      if (this.clientId) {
        localStorage.setItem(CLIENT_ID_KEY, this.clientId)
      } else {
        localStorage.removeItem(CLIENT_ID_KEY)
      }
    },
    logout() {
      this.clientId = ''
      this.apiKey = ''
      localStorage.removeItem(CLIENT_ID_KEY)
      sessionStorage.removeItem(API_KEY_KEY)
    },
  },
})
