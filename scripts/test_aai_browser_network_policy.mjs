#!/usr/bin/env node

import { createRequire } from 'node:module'
import { createServer } from 'node:http'
import { once } from 'node:events'
import { resolve } from 'node:path'
import { fileURLToPath } from 'node:url'

import { applyBrowserNetworkPolicy, browserContextOptions } from './aai_browser_network_policy.mjs'

const ROOT = resolve(fileURLToPath(new URL('..', import.meta.url)))
const requireFromFrontend = createRequire(resolve(ROOT, 'frontend/package.json'))
const { chromium } = requireFromFrontend('@playwright/test')

function listen(server) {
  server.listen(0, '127.0.0.1')
  return once(server, 'listening').then(() => server.address().port)
}

let blockedHttpRequests = 0
let blockedWebSocketUpgrades = 0
const blockedServer = createServer((_request, response) => {
  blockedHttpRequests += 1
  response.writeHead(204).end()
})
blockedServer.on('upgrade', (_request, socket) => {
  blockedWebSocketUpgrades += 1
  socket.destroy()
})

const allowedServer = createServer((request, response) => {
  if (request.url === '/sw.js') {
    response.writeHead(200, { 'content-type': 'application/javascript' })
    response.end("self.addEventListener('fetch', () => {})")
    return
  }
  response.writeHead(200, { 'content-type': 'text/html' })
  response.end('<!doctype html><title>policy test</title>')
})

const blockedPort = await listen(blockedServer)
const allowedPort = await listen(allowedServer)
const allowedOrigin = `http://127.0.0.1:${allowedPort}`
const blockedOrigin = `http://127.0.0.1:${blockedPort}`
const browser = await chromium.launch({ headless: true })

try {
  const context = await browser.newContext(browserContextOptions({
    viewport: { width: 800, height: 600 },
    locale: 'en-HK',
  }))
  await applyBrowserNetworkPolicy(context, allowedOrigin)
  const page = await context.newPage()
  await page.goto(allowedOrigin, { waitUntil: 'domcontentloaded' })

  const result = await page.evaluate(async ({ blockedOrigin }) => {
    const output = { fetchBlocked: false, webSocketBlocked: false, serviceWorkerBlocked: false }
    try {
      await fetch(`${blockedOrigin}/probe`)
    } catch {
      output.fetchBlocked = true
    }
    output.webSocketBlocked = await new Promise((resolveResult) => {
      const socket = new WebSocket(blockedOrigin.replace('http:', 'ws:') + '/ws')
      const timer = setTimeout(() => resolveResult(socket.readyState !== WebSocket.OPEN), 500)
      socket.addEventListener('open', () => {
        clearTimeout(timer)
        resolveResult(false)
      })
      socket.addEventListener('error', () => {
        clearTimeout(timer)
        resolveResult(true)
      })
    })
    try {
      const registration = await navigator.serviceWorker.register('/sw.js')
      await new Promise((resolveWait) => setTimeout(resolveWait, 100))
      output.serviceWorkerBlocked = registration.active === null
    } catch {
      output.serviceWorkerBlocked = true
    }
    output.serviceWorkerControlled = navigator.serviceWorker.controller !== null
    return output
  }, { blockedOrigin })

  await page.waitForTimeout(100)
  const facts = {
    ...result,
    serviceWorkerCount: context.serviceWorkers().length,
    blockedHttpRequests,
    blockedWebSocketUpgrades,
  }
  console.log(JSON.stringify(facts))
  if (
    !facts.fetchBlocked ||
    !facts.webSocketBlocked ||
    !facts.serviceWorkerBlocked ||
    facts.serviceWorkerControlled ||
    facts.serviceWorkerCount !== 0 ||
    facts.blockedHttpRequests !== 0 ||
    facts.blockedWebSocketUpgrades !== 0
  ) {
    process.exitCode = 1
  }
  await context.close()
} finally {
  await browser.close()
  allowedServer.close()
  blockedServer.close()
}
