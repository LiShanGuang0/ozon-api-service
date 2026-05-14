import { defineConfig, loadEnv } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, '.', '')
  const apiProxyTarget = env.VITE_API_PROXY_TARGET || 'http://127.0.0.1:8000'
  // 部署在子路径时设置 .env.production 中 VITE_APP_BASE=/ozon-service-merchant/，否则资源会请求到域名根 /assets/...
  const appBase = env.VITE_APP_BASE?.trim()
  const base =
    appBase && appBase !== '/'
      ? (appBase.endsWith('/') ? appBase : `${appBase}/`)
      : '/'

  return {
    base,
    plugins: [vue()],
    server: {
      port: 5173,
      proxy: {
        '/api': {
          target: apiProxyTarget,
          changeOrigin: true,
        },
      },
    },
  }
})
