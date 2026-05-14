import { App as CapacitorApp } from '@capacitor/app'
import { Capacitor } from '@capacitor/core'
import { ElMessage } from 'element-plus'
import type { Router } from 'vue-router'

const ROOT_ROUTES = new Set(['/dashboard', '/login'])

let registered = false
let lastExitAttemptAt = 0

export function registerNativeBackButton(router: Router) {
  if (registered || !Capacitor.isNativePlatform()) return
  registered = true

  CapacitorApp.addListener('backButton', async ({ canGoBack }) => {
    const currentPath = router.currentRoute.value.path

    if (!ROOT_ROUTES.has(currentPath)) {
      if (canGoBack && window.history.length > 1) {
        router.back()
        return
      }

      await router.replace('/dashboard')
      return
    }

    const now = Date.now()
    if (now - lastExitAttemptAt < 1600) {
      await CapacitorApp.exitApp()
      return
    }

    lastExitAttemptAt = now
    ElMessage.info('再按一次退出应用')
  })
}
