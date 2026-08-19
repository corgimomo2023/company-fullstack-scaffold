export function browserContextOptions(options = {}) {
  return { ...options, serviceWorkers: 'block' }
}

export async function applyBrowserNetworkPolicy(context, allowedOrigin) {
  const allowed = new URL(allowedOrigin)
  const allowedWebSocketOrigin = `${allowed.protocol === 'https:' ? 'wss:' : 'ws:'}//${allowed.host}`

  await context.route('**/*', async (route) => {
    const requestUrl = new URL(route.request().url())
    if (
      requestUrl.protocol === 'data:' ||
      requestUrl.protocol === 'blob:' ||
      requestUrl.origin === allowed.origin
    ) {
      await route.continue()
    } else {
      await route.abort('blockedbyclient')
    }
  })

  await context.routeWebSocket('**/*', async (webSocketRoute) => {
    const requestUrl = new URL(webSocketRoute.url())
    if (requestUrl.origin === allowedWebSocketOrigin) {
      webSocketRoute.connectToServer()
    } else {
      await webSocketRoute.close({ code: 1008, reason: 'Blocked by exact-origin audit policy' })
    }
  })
}
