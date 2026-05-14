import { Capacitor } from '@capacitor/core'
import { Device } from '@capacitor/device'

export interface AppDeviceIdentity {
  isNativeApp: boolean
  platform: string
  deviceId: string
  macAddress: string | null
}

export async function getAppDeviceIdentity(): Promise<AppDeviceIdentity> {
  const isNativeApp = Capacitor.isNativePlatform()
  if (!isNativeApp) {
    return {
      isNativeApp: false,
      platform: 'web',
      deviceId: '',
      macAddress: null,
    }
  }

  const [id, info] = await Promise.all([Device.getId(), Device.getInfo()])
  return {
    isNativeApp: true,
    platform: info.platform,
    deviceId: id.identifier,
    macAddress: null,
  }
}
