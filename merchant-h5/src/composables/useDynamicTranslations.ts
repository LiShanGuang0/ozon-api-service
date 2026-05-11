import { ref } from 'vue'

import { translateTexts } from '../api/merchant'
import { useI18n } from '../i18n'

const cache = new Map<string, string>()

function cacheKey(locale: string, text: string) {
  return `${locale}::${text}`
}

function cleanTexts(texts: Array<string | null | undefined>) {
  return Array.from(
    new Set(
      texts
        .map((text) => text?.trim())
        .filter((text): text is string => Boolean(text)),
    ),
  )
}

export function useDynamicTranslations() {
  const { locale, messageText } = useI18n()
  const version = ref(0)

  function translatedText(text?: string | null) {
    if (!text) return ''
    const value = version.value
    void value

    const normalized = text.trim()
    const businessText = messageText(normalized)
    if (businessText !== normalized) return businessText

    return cache.get(cacheKey(locale.value, normalized)) || normalized
  }

  async function ensureTranslations(texts: Array<string | null | undefined>) {
    const target = locale.value
    const missing = cleanTexts(texts).filter((text) => {
      if (messageText(text) !== text) return false
      return !cache.has(cacheKey(target, text))
    })

    if (!missing.length) return

    try {
      const result = await translateTexts({
        texts: missing,
        target_language: target,
        source_language: 'auto',
      })
      for (const item of result.items) {
        cache.set(cacheKey(item.target_language, item.text), item.translated_text || item.text)
      }
    } catch {
      for (const text of missing) {
        cache.set(cacheKey(target, text), text)
      }
    } finally {
      version.value += 1
    }
  }

  return {
    locale,
    ensureTranslations,
    translatedText,
  }
}
