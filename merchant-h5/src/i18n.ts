import { computed, ref } from 'vue'

export type Locale = 'zh' | 'ru' | 'en'

const LOCALE_KEY = 'ozon-merchant-locale'
const savedLocale = localStorage.getItem(LOCALE_KEY) as Locale | null
const locale = ref<Locale>(savedLocale && ['zh', 'ru', 'en'].includes(savedLocale) ? savedLocale : 'zh')

const dictionaries: Record<Locale, Record<string, string>> = {
  zh: {
    appName: 'Ozon 推送台',
    merchantConsole: 'Merchant Console',
    cockpitTitle: '商户推送驾驶舱',
    cockpitSubtitle: '一屏查看商品推送进度、任务结果、失败提醒和终端控制台。',
    workspace: '工作台',
    detailSubtitle: '查看当前商户的数据详情',
    switchAccount: '切换账号',
    currentStatus: '当前状态',
    connected: '连接正常',
    terminalConsole: '终端控制台',
    refreshing: '实时刷新中',
    paused: '已暂停',
    todayCount: '今日 {count} 条',
    readingConsole: '正在读取控制台日志',
    emptyConsole: '暂无控制台日志',
    products: '商品列表',
    productsDesc: '查看已推送商品、Ozon ID、SKU 和同步状态',
    merchantInfo: '商户信息',
    merchantInfoDesc: '查看店铺资料、默认仓库和连接状态',
    productStatus: '商品状态',
    productStatusDesc: '按 Ozon 同步状态统计当前商品',
    productListTitle: '商品列表',
    productListDesc: '查看当前商户已推送到 Ozon 的商品状态',
    searchProduct: '搜索 offer_id / 商品名',
    status: '状态',
    query: '查询',
    offerId: '商品货号',
    productImage: '商品图片',
    productName: '商品名称',
    ozonProductId: 'Ozon商品ID',
    price: '价格',
    lastTask: '最近任务',
    updatedAt: '更新时间',
    taskStatus: '任务状态',
    partialSuccess: '部分成功',
    taskId: '任务ID',
    productCount: '商品数',
    success: '成功',
    failed: '失败',
    submittedAt: '提交时间',
    action: '操作',
    view: '查看',
    taskDetail: '任务详情',
    finishedAt: '完成时间',
    errorInfo: '错误信息',
    unknown: '未知',
    draft: '草稿',
    pending: '处理中',
    running: '执行中',
    imported: '已成功',
    skipped: '商品数据创建重复（跳过）',
    info: '提示',
    archived: '已归档',
    active: '正常',
    today_tasks: '今日推送',
    success_tasks: '成功任务',
    failed_tasks: '失败任务',
    pending_tasks: '处理中',
    credentialLogin: '凭证校验',
    loginBrand: 'Ozon 商户推送台',
    loginSubtitle: '输入店铺凭证后进入驾驶舱',
    connectShop: '连接 Ozon 店铺',
    loginDesc: '系统会先查询本地商户资料；若没有记录，将调用 Ozon 接口初始化店铺信息。',
    clientIdPlaceholder: '请输入 Ozon Client-Id',
    apiKeyPlaceholder: '请输入 Ozon Api-Key',
    enterCockpit: '进入驾驶舱',
    loginNote: 'Api-Key 仅保存在当前浏览器会话，用于校验和后续 Ozon 接口请求。',
    credentialRequired: '请填写 Client-Id 和 Api-Key',
    initializedFromOzon: '已从 Ozon 初始化店铺资料',
    credentialPassed: '凭证校验通过',
    merchantInfoPageDesc: '用于 H5 展示和数据隔离的商户资料',
    merchantId: '商户ID',
    shopName: '店铺名称',
    currency: '币种',
    defaultWarehouse: '默认仓库',
    contactName: '联系人',
    contactPhone: '联系电话',
    contactEmail: '联系邮箱',
    lastConnected: '最近连接',
    lastError: '最近错误',
  },
  en: {
    appName: 'Ozon Push Console',
    merchantConsole: 'Merchant Console',
    cockpitTitle: 'Merchant Push Cockpit',
    cockpitSubtitle: 'Monitor product pushes, task results, failure alerts, and the terminal console.',
    workspace: 'Workspace',
    detailSubtitle: 'View current merchant data details',
    switchAccount: 'Switch Account',
    currentStatus: 'Current Status',
    connected: 'Connected',
    terminalConsole: 'Terminal Console',
    refreshing: 'Live refresh',
    paused: 'Paused',
    todayCount: 'Today {count}',
    readingConsole: 'Reading console logs',
    emptyConsole: 'No console logs',
    products: 'Products',
    productsDesc: 'View pushed products, Ozon ID, SKU, and sync status',
    merchantInfo: 'Merchant Info',
    merchantInfoDesc: 'View shop profile, default warehouse, and connection status',
    productStatus: 'Product Status',
    productStatusDesc: 'Product counts by Ozon sync status',
    productListTitle: 'Products',
    productListDesc: 'View product status pushed to Ozon for this merchant',
    searchProduct: 'Search offer_id / product name',
    status: 'Status',
    query: 'Search',
    offerId: 'Offer ID',
    productImage: 'Image',
    productName: 'Product Name',
    ozonProductId: 'Ozon Product ID',
    price: 'Price',
    lastTask: 'Last Task',
    updatedAt: 'Updated At',
    taskStatus: 'Task Status',
    partialSuccess: 'Partial Success',
    taskId: 'Task ID',
    productCount: 'Products',
    success: 'Success',
    failed: 'Failed',
    submittedAt: 'Submitted At',
    action: 'Action',
    view: 'View',
    taskDetail: 'Task Detail',
    finishedAt: 'Finished At',
    errorInfo: 'Error Info',
    unknown: 'Unknown',
    draft: 'Draft',
    pending: 'Processing',
    running: 'Running',
    imported: 'Succeeded',
    import_pending: 'Product creation processing',
    stock_updated: 'Stock updated',
    attributes_synced: 'Attributes synced',
    stock_synced: 'Stock checked',
    completed: 'Full workflow completed',
    skipped: 'Duplicate product data creation (skipped)',
    info: 'Info',
    archived: 'Archived',
    active: 'Normal',
    today_tasks: 'Today Pushes',
    success_tasks: 'Successful Tasks',
    failed_tasks: 'Failed Tasks',
    pending_tasks: 'Processing',
    credentialLogin: 'Credential Check',
    loginBrand: 'Ozon Merchant Console',
    loginSubtitle: 'Enter shop credentials to open the cockpit',
    connectShop: 'Connect Ozon Shop',
    loginDesc: 'The system checks local merchant data first. If none exists, it initializes shop information from Ozon.',
    clientIdPlaceholder: 'Enter Ozon Client-Id',
    apiKeyPlaceholder: 'Enter Ozon Api-Key',
    enterCockpit: 'Enter Cockpit',
    loginNote: 'Api-Key is stored only in this browser session for validation and Ozon API requests.',
    credentialRequired: 'Please enter Client-Id and Api-Key',
    initializedFromOzon: 'Shop profile initialized from Ozon',
    credentialPassed: 'Credentials verified',
    merchantInfoPageDesc: 'Merchant profile for H5 display and data isolation',
    merchantId: 'Merchant ID',
    shopName: 'Shop Name',
    currency: 'Currency',
    defaultWarehouse: 'Default Warehouse',
    contactName: 'Contact',
    contactPhone: 'Phone',
    contactEmail: 'Email',
    lastConnected: 'Last Connected',
    lastError: 'Last Error',
  },
  ru: {
    appName: 'Панель Ozon',
    merchantConsole: 'Merchant Console',
    cockpitTitle: 'Панель продавца',
    cockpitSubtitle: 'Контроль отправки товаров, задач, ошибок и терминальной консоли.',
    workspace: 'Рабочая панель',
    detailSubtitle: 'Данные текущего продавца',
    switchAccount: 'Сменить аккаунт',
    currentStatus: 'Статус',
    connected: 'Подключено',
    terminalConsole: 'Терминал',
    refreshing: 'Автообновление',
    paused: 'Пауза',
    todayCount: 'Сегодня {count}',
    readingConsole: 'Чтение логов',
    emptyConsole: 'Логов нет',
    products: 'Товары',
    productsDesc: 'Товары, Ozon ID, SKU и статус синхронизации',
    merchantInfo: 'Информация',
    merchantInfoDesc: 'Профиль магазина, склад и статус подключения',
    productStatus: 'Статусы товаров',
    productStatusDesc: 'Статистика товаров по статусам Ozon',
    productListTitle: 'Товары',
    productListDesc: 'Статусы товаров, отправленных в Ozon',
    searchProduct: 'Поиск offer_id / название',
    status: 'Статус',
    query: 'Поиск',
    offerId: 'Артикул',
    productImage: 'Фото',
    productName: 'Название',
    ozonProductId: 'Ozon ID',
    price: 'Цена',
    lastTask: 'Последняя задача',
    updatedAt: 'Обновлено',
    taskStatus: 'Статус задачи',
    partialSuccess: 'Частично успешно',
    taskId: 'ID задачи',
    productCount: 'Товары',
    success: 'Успешно',
    failed: 'Ошибка',
    submittedAt: 'Отправлено',
    action: 'Действие',
    view: 'Открыть',
    taskDetail: 'Детали задачи',
    finishedAt: 'Завершено',
    errorInfo: 'Ошибка',
    unknown: 'Неизвестно',
    draft: 'Черновик',
    pending: 'В обработке',
    running: 'Выполняется',
    imported: 'Успешно',
    skipped: 'Дубликат при создании товара (пропущено)',
    info: 'Инфо',
    archived: 'В архиве',
    active: 'Норма',
    today_tasks: 'Сегодня отправлено',
    success_tasks: 'Успешные задачи',
    failed_tasks: 'Ошибки',
    pending_tasks: 'В обработке',
    credentialLogin: 'Проверка ключей',
    loginBrand: 'Панель продавца Ozon',
    loginSubtitle: 'Введите ключи магазина для входа',
    connectShop: 'Подключить магазин Ozon',
    loginDesc: 'Сначала проверяются локальные данные продавца. Если их нет, профиль будет создан по данным Ozon.',
    clientIdPlaceholder: 'Введите Ozon Client-Id',
    apiKeyPlaceholder: 'Введите Ozon Api-Key',
    enterCockpit: 'Открыть панель',
    loginNote: 'Api-Key хранится только в текущей сессии браузера для проверки и запросов к Ozon.',
    credentialRequired: 'Введите Client-Id и Api-Key',
    initializedFromOzon: 'Профиль магазина создан из Ozon',
    credentialPassed: 'Ключи проверены',
    merchantInfoPageDesc: 'Профиль продавца для отображения H5 и разделения данных',
    merchantId: 'ID продавца',
    shopName: 'Название магазина',
    currency: 'Валюта',
    defaultWarehouse: 'Склад по умолчанию',
    contactName: 'Контакт',
    contactPhone: 'Телефон',
    contactEmail: 'Email',
    lastConnected: 'Последнее подключение',
    lastError: 'Последняя ошибка',
  },
}

const extraDictionary: Record<Locale, Record<string, string>> = {
  zh: {
    inventoryInfo: '库存信息',
    warehouseId: '仓库 ID',
    warehouseName: '仓库',
    stockQty: '库存',
    reservedStock: '占用',
  },
  en: {
    inventoryInfo: 'Inventory',
    warehouseId: 'Warehouse ID',
    warehouseName: 'Warehouse',
    stockQty: 'Stock',
    reservedStock: 'Reserved',
  },
  ru: {
    inventoryInfo: 'Остатки',
    warehouseId: 'ID склада',
    warehouseName: 'Склад',
    stockQty: 'Остаток',
    reservedStock: 'Зарезервировано',
  },
}

const messageMap: Record<string, Record<Locale, string>> = {
  '商品推送完整链路完成': {
    zh: '商品推送完整链路完成',
    en: 'Product push workflow completed',
    ru: 'Полная цепочка отправки товара завершена',
  },
  '开始查询商品创建额度': {
    zh: '开始查询商品创建额度',
    en: 'Querying product creation quota',
    ru: 'Запрос лимита создания товаров',
  },
  '商品创建额度查询完成': {
    zh: '商品创建额度查询完成',
    en: 'Product creation quota query completed',
    ru: 'Лимит создания товаров получен',
  },
  '商品数据已提交至 Ozon': {
    zh: '商品数据已提交至 Ozon',
    en: 'Product data submitted to Ozon',
    ru: 'Данные товара отправлены в Ozon',
  },
  'Ozon 推送任务建立成功，等待平台处理': {
    zh: 'Ozon 推送任务建立成功，等待平台处理',
    en: 'Ozon push task created, waiting for platform processing',
    ru: 'Задача отправки Ozon создана, ожидание обработки',
  },
  '商品数据创建完成': {
    zh: '商品数据创建完成',
    en: 'Product data creation completed',
    ru: 'Создание данных товара завершено',
  },
  '商品数据创建失败': {
    zh: '商品数据创建失败',
    en: 'Product data creation failed',
    ru: 'Ошибка создания данных товара',
  },
  '商品数据创建重复（跳过）': {
    zh: '商品数据创建重复（跳过）',
    en: 'Duplicate product data creation (skipped)',
    ru: 'Дубликат при создании товара (пропущено)',
  },
  '商品数据创建处理中': {
    zh: '商品数据创建处理中',
    en: 'Product data creation in progress',
    ru: 'Создание данных товара выполняется',
  },
  '商品数据推送失败': {
    zh: '商品数据推送失败',
    en: 'Product data push failed',
    ru: 'Ошибка отправки данных товара',
  },
  '开始查询商品类目树': {
    zh: '开始查询商品类目树',
    en: 'Querying product category tree',
    ru: 'Запрос дерева категорий товаров',
  },
  '商品类目树查询完成': {
    zh: '商品类目树查询完成',
    en: 'Product category tree query completed',
    ru: 'Дерево категорий товаров получено',
  },
  '开始查询商品类目属性': {
    zh: '开始查询商品类目属性',
    en: 'Querying product category attributes',
    ru: 'Запрос атрибутов категории',
  },
  '商品类目属性查询完成': {
    zh: '商品类目属性查询完成',
    en: 'Product category attributes query completed',
    ru: 'Атрибуты категории получены',
  },
  '开始查询商品属性字典值': {
    zh: '开始查询商品属性字典值',
    en: 'Querying product attribute dictionary values',
    ru: 'Запрос значений справочника атрибута',
  },
  '商品属性字典值查询完成': {
    zh: '商品属性字典值查询完成',
    en: 'Product attribute dictionary values query completed',
    ru: 'Значения справочника атрибута получены',
  },
  '库存更新任务已建立，开始处理': {
    zh: '库存更新任务已建立，开始处理',
    en: 'Stock update task created, processing started',
    ru: 'Задача обновления остатков создана',
  },
  '商品库存更新完成': {
    zh: '商品库存更新完成',
    en: 'Product stock update completed',
    ru: 'Остаток товара обновлен',
  },
  '商品库存更新失败': {
    zh: '商品库存更新失败',
    en: 'Product stock update failed',
    ru: 'Ошибка обновления остатка товара',
  },
  '商品归档完成': {
    zh: '商品归档完成',
    en: 'Product archived',
    ru: 'Товар архивирован',
  },
  '商品归档失败': {
    zh: '商品归档失败',
    en: 'Product archive failed',
    ru: 'Ошибка архивирования товара',
  },
  '商品还原完成': {
    zh: '商品还原完成',
    en: 'Product restored from archive',
    ru: 'Товар восстановлен из архива',
  },
  '商品还原失败': {
    zh: '商品还原失败',
    en: 'Product restore failed',
    ru: 'Ошибка восстановления товара',
  },
}

function normalizeStatus(status?: string | null) {
  if (status === 'success') return 'success'
  if (status === 'failed') return 'failed'
  if (status === 'partial') return 'partialSuccess'
  return status || 'unknown'
}

export function setLocale(value: Locale) {
  locale.value = value
  localStorage.setItem(LOCALE_KEY, value)
}

export function useI18n() {
  const currentLocale = computed(() => locale.value)
  const t = (key: string, vars?: Record<string, string | number>) => {
    let text = extraDictionary[locale.value][key] || extraDictionary.zh[key] || dictionaries[locale.value][key] || dictionaries.zh[key] || key
    if (vars) {
      Object.entries(vars).forEach(([name, value]) => {
        text = text.replace(`{${name}}`, String(value))
      })
    }
    return text
  }
  const statusText = (status?: string | null, fallback?: string | null) => {
    const key = normalizeStatus(status)
    const workflowText: Record<string, Record<Locale, string>> = {
      import_pending: {
        zh: '商品创建处理中',
        en: 'Product creation processing',
        ru: 'Создание товара выполняется',
      },
      stock_updated: {
        zh: '库存设置完成',
        en: 'Stock updated',
        ru: 'Остаток обновлен',
      },
      attributes_synced: {
        zh: '属性同步完成',
        en: 'Attributes synced',
        ru: 'Атрибуты синхронизированы',
      },
      stock_synced: {
        zh: '库存查询完成',
        en: 'Stock checked',
        ru: 'Остаток проверен',
      },
      completed: {
        zh: '完整链路完成',
        en: 'Full workflow completed',
        ru: 'Полная цепочка завершена',
      },
    }
    if (workflowText[key]) return workflowText[key][locale.value]
    return dictionaries[locale.value][key] || fallback || status || t('unknown')
  }
  const messageText = (message?: string | null): string => {
    if (!message) return ''
    if (messageMap[message]) return messageMap[message][locale.value]
    if (message.startsWith('任务查询成功，当前处理结果：')) {
      const result = message.replace('任务查询成功，当前处理结果：', '')
      return {
        zh: message,
        en: `Task query completed. Current result: ${messageText(result)}`,
        ru: `Запрос задачи выполнен. Результат: ${messageText(result)}`,
      }[locale.value]
    }
    if (message.startsWith('商品归档处理完成：')) {
      return {
        zh: message,
        en: message.replace('商品归档处理完成：', 'Product archive completed: ').replace('成功', 'success').replace('失败', 'failed').replace('跳过', 'skipped'),
        ru: message.replace('商品归档处理完成：', 'Архивирование завершено: ').replace('成功', 'успешно').replace('失败', 'ошибки').replace('跳过', 'пропущено'),
      }[locale.value]
    }
    if (message.startsWith('商品还原处理完成：')) {
      return {
        zh: message,
        en: message.replace('商品还原处理完成：', 'Product restore completed: ').replace('成功', 'success').replace('失败', 'failed').replace('跳过', 'skipped'),
        ru: message.replace('商品还原处理完成：', 'Восстановление завершено: ').replace('成功', 'успешно').replace('失败', 'ошибки').replace('跳过', 'пропущено'),
      }[locale.value]
    }
    if (message.startsWith('库存更新处理完成：')) {
      return {
        zh: message,
        en: message.replace('库存更新处理完成：', 'Stock update completed: ').replace('成功', 'success').replace('失败', 'failed'),
        ru: message.replace('库存更新处理完成：', 'Обновление остатков завершено: ').replace('成功', 'успешно').replace('失败', 'ошибки'),
      }[locale.value]
    }
    if (message.includes('SPU_ALREADY_EXISTS_IN_ANOTHER_ACCOUNT') || message.includes('дублируется')) {
      return {
        zh: '相同商品已存在于其他店铺或商品卡片中',
        en: 'The same product already exists in another account or product card',
        ru: message,
      }[locale.value]
    }
    return message
  }

  return { locale: currentLocale, setLocale, t, statusText, messageText }
}
