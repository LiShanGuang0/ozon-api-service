import { defineStore } from 'pinia'

const CLIENT_ID_KEY = 'ozon-merchant-client-id'
const API_KEY_KEY = 'ozon-merchant-api-key'

type ActivationStatus = 'unknown' | 'checking' | 'required' | 'active'

export const useMerchantStore = defineStore('merchant', {
  state: () => ({
    clientId: '',
    apiKey: '',
    runtimeInitialized: false,
    isNativeApp: false,
    appPlatform: 'web',
    deviceId: '',
    macAddress: null as string | null,
    activationStatus: 'unknown' as ActivationStatus,
    activationReason: null as string | null,
    activationExpiresAt: null as string | null,
  }),
  getters: {
    isAppReady: (state) => Boolean(state.isNativeApp && state.clientId && state.activationStatus === 'active'),
    isReady: (state) =>
      state.isNativeApp
        ? Boolean(state.clientId && state.activationStatus === 'active')
        : Boolean(state.clientId && state.apiKey),
  },
  actions: {
    setAppIdentity(identity: {
      isNativeApp: boolean
      platform: string
      deviceId: string
      macAddress: string | null
    }) {
      this.runtimeInitialized = true
      this.isNativeApp = identity.isNativeApp
      this.appPlatform = identity.platform
      this.deviceId = identity.deviceId
      this.macAddress = identity.macAddress
      if (!identity.isNativeApp) {
        this.activationStatus = 'unknown'
        this.activationReason = null
        this.activationExpiresAt = null
      }
    },
    setActivationChecking() {
      this.activationStatus = 'checking'
      this.activationReason = null
    },
    setActivationRequired(reason?: string | null, clientId?: string | null, expiresAt?: string | null) {
      this.activationStatus = 'required'
      this.activationReason = reason || null
      this.activationExpiresAt = expiresAt || null
      if (clientId) {
        this.setClientId(clientId)
      }
    },
    setActivationActive(clientId: string, expiresAt?: string | null) {
      this.activationStatus = 'active'
      this.activationReason = null
      this.activationExpiresAt = expiresAt || null
      this.setClientId(clientId)
    },
    setCredentials(clientId: string, apiKey: string) {
      this.clientId = clientId.trim()
      this.apiKey = apiKey.trim()
      if (this.isNativeApp && this.clientId) {
        localStorage.setItem(CLIENT_ID_KEY, this.clientId)
      } else {
        localStorage.removeItem(CLIENT_ID_KEY)
      }
      sessionStorage.removeItem(API_KEY_KEY)
    },
    setClientId(value: string) {
      this.clientId = value.trim()
      if (this.isNativeApp && this.clientId) {
        localStorage.setItem(CLIENT_ID_KEY, this.clientId)
      } else {
        localStorage.removeItem(CLIENT_ID_KEY)
      }
    },
    logout() {
      this.clientId = ''
      this.apiKey = ''
      this.activationStatus = this.isNativeApp ? 'required' : 'unknown'
      this.activationReason = null
      this.activationExpiresAt = null
      localStorage.removeItem(CLIENT_ID_KEY)
      sessionStorage.removeItem(API_KEY_KEY)
    },
  },
})
