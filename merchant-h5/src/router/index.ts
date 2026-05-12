import { createRouter, createWebHistory } from 'vue-router'
import { useMerchantStore } from '../stores/merchant'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/login',
      name: 'login',
      component: () => import('../views/Login.vue'),
      meta: { title: '凭证登录', titleKey: 'workspace', public: true },
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

router.beforeEach((to) => {
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
