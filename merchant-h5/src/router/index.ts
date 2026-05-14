import { createRouter, createWebHistory } from 'vue-router'

import { checkActivation } from '../api/merchant'
import { useMerchantStore } from '../stores/merchant'
import { getAppDeviceIdentity } from '../utils/appRuntime'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/login',
      name: 'login',
      component: () => import('../views/Login.vue'),
      meta: { title: '凭证登录', titleKey: 'workspace', public: true },
    },
    {
      path: '/activation-admin',
      name: 'activation-admin',
      component: () => import('../views/ActivationAdmin.vue'),
      meta: { title: '激活管理', public: true, standalone: true, skipActivationCheck: true },
    },
    {
      path: '/',
      redirect: '/dashboard',
    },
    {
      path: '/dashboard',
      name: 'dashboard',
      component: () => import('../views/Dashboard.vue'),
      meta: { title: '工作台', titleKey: 'workspace' },
    },
    {
      path: '/products',
      name: 'products',
      component: () => import('../views/Products.vue'),
      meta: { title: '商品列表', titleKey: 'products' },
    },
    {
      path: '/merchant',
      name: 'merchant',
      component: () => import('../views/MerchantProfile.vue'),
      meta: { title: '商户信息', titleKey: 'merchantInfo' },
    },
  ],
})

async function ensureRuntime() {
  const merchant = useMerchantStore()
  if (merchant.runtimeInitialized) return
  merchant.setAppIdentity(await getAppDeviceIdentity())
}

async function ensureAppActivation() {
  const merchant = useMerchantStore()
  if (!merchant.isNativeApp || merchant.activationStatus === 'active' || merchant.activationStatus === 'required') {
    return
  }
  if (!merchant.deviceId) {
    merchant.setActivationRequired('missing_device_id')
    return
  }

  merchant.setActivationChecking()
  try {
    const result = await checkActivation({
      device_id: merchant.deviceId,
      mac_address: merchant.macAddress,
    })
    if (result.bound && result.client_id) {
      merchant.setActivationActive(result.client_id, result.expires_at)
    } else {
      merchant.setActivationRequired(result.reason, result.client_id, result.expires_at)
    }
  } catch {
    merchant.setActivationRequired('check_failed')
  }
}

router.beforeEach(async (to) => {
  await ensureRuntime()
  if (!to.meta.skipActivationCheck) {
    await ensureAppActivation()
  }

  const merchant = useMerchantStore()
  if (!to.meta.public && !merchant.isReady) {
    return '/login'
  }
  if (to.path === '/login' && merchant.isReady) {
    return '/dashboard'
  }
  return true
})

export default router
