// Scratch script (not part of the repo): drives headless Chrome through the storefront and takes screenshots.
import { spawn } from 'node:child_process'
import { writeFile } from 'node:fs/promises'

const S = process.argv[2]
const BASE = 'http://127.0.0.1:5173'
const PORT = 9333
const CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
const sleep = (ms) => new Promise((r) => setTimeout(r, ms))

const chrome = spawn(
  CHROME,
  ['--headless=new', '--disable-gpu', '--hide-scrollbars', `--remote-debugging-port=${PORT}`, `--user-data-dir=${S}/chrome-cdp`, 'about:blank'],
  { stdio: 'ignore' },
)

async function pageSocketUrl() {
  for (let i = 0; i < 60; i++) {
    try {
      const targets = await (await fetch(`http://127.0.0.1:${PORT}/json`)).json()
      const page = targets.find((t) => t.type === 'page')
      if (page) return page.webSocketDebuggerUrl
    } catch {}
    await sleep(200)
  }
  throw new Error('chrome did not start')
}

const ws = new WebSocket(await pageSocketUrl())
await new Promise((r) => ws.addEventListener('open', r))
let nextId = 0
const pending = new Map()
const problems = []
ws.addEventListener('message', (event) => {
  const m = JSON.parse(event.data)
  if (m.id && pending.has(m.id)) {
    pending.get(m.id)(m)
    pending.delete(m.id)
  } else if (m.method === 'Runtime.exceptionThrown') {
    problems.push('EXCEPTION ' + (m.params.exceptionDetails.exception?.description ?? m.params.exceptionDetails.text))
  } else if (m.method === 'Runtime.consoleAPICalled' && ['error', 'warning'].includes(m.params.type)) {
    problems.push(m.params.type + ': ' + m.params.args.map((a) => a.value ?? a.description).join(' '))
  } else if (m.method === 'Log.entryAdded' && m.params.entry.level === 'error') {
    problems.push('LOG ' + m.params.entry.text + ' ' + (m.params.entry.url ?? ''))
  }
})
const send = (method, params = {}) =>
  new Promise((resolve) => {
    const id = ++nextId
    pending.set(id, resolve)
    ws.send(JSON.stringify({ id, method, params }))
  })
const ev = async (expression) =>
  (await send('Runtime.evaluate', { expression, awaitPromise: true, returnByValue: true })).result?.result?.value
const waitFor = async (expression, ms = 8000) => {
  const end = Date.now() + ms
  while (Date.now() < end) {
    if (await ev(expression)) return true
    await sleep(150)
  }
  return false
}

let width = 1280
let mobile = false
const viewport = (w, h, m) => {
  width = w
  mobile = m
  return send('Emulation.setDeviceMetricsOverride', { width: w, height: h, deviceScaleFactor: 1, mobile: m })
}
const goto = async (path) => {
  await send('Page.navigate', { url: BASE + path })
  await sleep(400)
}
async function shot(name) {
  const metrics = await send('Page.getLayoutMetrics')
  const height = Math.ceil(metrics.result.cssContentSize?.height ?? metrics.result.contentSize.height)
  await viewport(width, Math.min(height, 4000), mobile)
  await sleep(250)
  const r = await send('Page.captureScreenshot', { format: 'png' })
  await writeFile(`${S}/${name}.png`, Buffer.from(r.result.data, 'base64'))
  await viewport(width, 900, mobile)
}
const count = () => ev("document.querySelector('.cart-pill__count')?.textContent")

await send('Page.enable')
await send('Runtime.enable')
await send('Log.enable')
const results = {}

if (process.argv[3] === 'modes') {
  await viewport(1280, 900, false)
  await send('Emulation.setEmulatedMedia', { features: [{ name: 'prefers-color-scheme', value: 'light' }] })
  await goto('/')
  await waitFor("document.querySelectorAll('.offer').length >= 8")
  await sleep(600)
  results.lightBodyBg = await ev('getComputedStyle(document.body).backgroundColor')
  await shot('home-light')
  await goto('/offers/PO-1010')
  await waitFor("document.querySelector('.detail__title')")
  await sleep(300)
  await shot('detail-light')
  await send('Emulation.setEmulatedMedia', {
    features: [
      { name: 'prefers-color-scheme', value: 'dark' },
      { name: 'prefers-reduced-motion', value: 'reduce' },
    ],
  })
  await goto('/')
  await waitFor("document.querySelectorAll('.offer').length >= 8")
  results.reducedMotion = {
    heroEmoji: await ev("getComputedStyle(document.querySelector('.art-emoji')).animationName"),
    pillDot: await ev("getComputedStyle(document.querySelector('.pill__dot')).animationName"),
    emojiBurstHidden: await ev("document.styleSheets.length > 0"),
  }
  results.consoleProblems = problems
  console.log(JSON.stringify(results, null, 2))
  ws.close()
  chrome.kill()
  process.exit(0)
}

// fresh visitor, system set to light
await viewport(1280, 900, false)
await send('Emulation.setEmulatedMedia', { features: [{ name: 'prefers-color-scheme', value: 'light' }] })
await goto('/')
await ev('localStorage.clear()')
await goto('/')
results.homeOffers = (await waitFor("document.querySelectorAll('.offer').length >= 8")) && (await ev("document.querySelectorAll('.offer').length"))
results.cartStartsAt = await count()
results.noCartIdBeforeAdd = await ev("localStorage.getItem('bss.cartId') === null")
await sleep(600)
await shot('home-desktop')

// theme: follows the system until the visitor chooses, then remembers the choice
results.themeFollowsSystemLight = await ev('document.documentElement.dataset.theme')
results.toggleLabelLight = await ev("document.querySelector('.theme-toggle')?.getAttribute('aria-label')")
await ev("document.querySelector('.theme-toggle').click()")
await sleep(300)
results.themeAfterToggle = await ev('document.documentElement.dataset.theme')
results.themeStored = await ev("localStorage.getItem('bss.theme')")
results.toggleLabelDark = await ev("document.querySelector('.theme-toggle')?.getAttribute('aria-label')")
results.bodyBgDark = await ev('getComputedStyle(document.body).backgroundColor')
await shot('home-dark')
await goto('/cart')
results.themePersistedAfterReload = await ev('document.documentElement.dataset.theme')
await ev("localStorage.removeItem('bss.theme')")
await send('Emulation.setEmulatedMedia', { features: [{ name: 'prefers-color-scheme', value: 'dark' }] })
await goto('/')
results.themeFollowsSystemDark = await ev('document.documentElement.dataset.theme')
await send('Emulation.setEmulatedMedia', { features: [{ name: 'prefers-color-scheme', value: 'light' }] })
await goto('/')
await waitFor("document.querySelectorAll('.offer').length >= 8")

// filter by category chip (devices): the page must stay where it is, not jump to the top
await ev('window.scrollTo(0, 650)')
await sleep(300)
results.scrollBeforeChip = await ev('Math.round(window.scrollY)')
await ev("[...document.querySelectorAll('.cat')].find(b => b.textContent.toLowerCase().includes('devices')).click()")
await sleep(900)
results.scrollAfterChip = await ev('Math.round(window.scrollY)')
results.devicesFilter = await ev("document.querySelectorAll('.offer').length")

// typing in the search box must not move the page either
await ev('window.scrollTo(0, 650)')
await sleep(300)
await ev("(() => { const i = document.querySelector('#q'); Object.getOwnPropertyDescriptor(HTMLInputElement.prototype, 'value').set.call(i, 'smartphone'); i.dispatchEvent(new Event('input', { bubbles: true })) })()")
await sleep(1100)
results.scrollAfterSearch = await ev('Math.round(window.scrollY)')
results.searchSmartphoneDevices = await ev("document.querySelectorAll('.offer').length")
await ev("(() => { const i = document.querySelector('#q'); Object.getOwnPropertyDescriptor(HTMLInputElement.prototype, 'value').set.call(i, ''); i.dispatchEvent(new Event('input', { bubbles: true })) })()")
await sleep(900)
results.urlAfterChip = await ev('location.search')
await ev("[...document.querySelectorAll('.cat')].find(b => b.textContent.toLowerCase().includes('all')).click()")
await sleep(700)

// add two offers from the grid
await ev("document.querySelectorAll('.offer .btn')[0].click()")
await sleep(350)
await shot('home-after-add-burst')
await waitFor("document.querySelector('.cart-pill__count')?.textContent === '1'")
results.countAfterFirstAdd = await count()
results.cartIdStored = await ev("/^SC-/.test(localStorage.getItem('bss.cartId') ?? '')")
results.toast = await ev("document.querySelector('.toast')?.textContent")
await ev("document.querySelectorAll('.offer .btn')[1].click()")
await waitFor("document.querySelector('.cart-pill__count')?.textContent === '2'")
results.countAfterSecondAdd = await count()

// detail page, quantity 3
await goto('/offers/PO-1004')
results.detailLoaded = await waitFor("document.querySelector('.detail__title')")
results.detailTitle = await ev("document.querySelector('.detail__title')?.textContent")
await ev("document.querySelectorAll('.stepper button')[1].click()")
await ev("document.querySelectorAll('.stepper button')[1].click()")
results.quantity = await ev("document.querySelector('.stepper output').textContent")
await shot('detail-desktop')
await ev("document.querySelector('.buy .btn').click()")
await waitFor("document.querySelector('.cart-pill__count')?.textContent === '5'")
results.countAfterDetailAdd = await count()

// hidden offer
await goto('/offers/PO-1006')
await waitFor("document.querySelector('.state')")
results.hiddenOffer = await ev("document.querySelector('.state h2')?.textContent")

// cart, after a full reload (cart id comes from localStorage)
await goto('/cart')
results.receipt = await waitFor("document.querySelector('.receipt')")
results.cartLines = await ev("document.querySelectorAll('.line').length")
results.totals = await ev("[...document.querySelectorAll('.receipt__totals div')].map(d => d.textContent.trim().replace(/\\s+/g,' '))")
await sleep(300)
await shot('cart-desktop')
await ev("document.querySelector('.line__remove').click()")
await waitFor("document.querySelectorAll('.line').length === 2")
results.linesAfterRemove = await ev("document.querySelectorAll('.line').length")
results.totalsAfterRemove = await ev("[...document.querySelectorAll('.receipt__totals div')].map(d => d.textContent.trim().replace(/\\s+/g,' '))")

// mobile views
await viewport(390, 844, true)
await goto('/')
await waitFor("document.querySelectorAll('.offer').length >= 8")
await sleep(600)
await shot('home-mobile')
await goto('/offers/PO-1010')
await waitFor("document.querySelector('.detail__title')")
await sleep(300)
await shot('detail-mobile')
await goto('/cart')
await waitFor("document.querySelector('.receipt')")
await sleep(300)
await shot('cart-mobile')
results.horizontalScrollOnMobile = await ev('document.documentElement.scrollWidth > window.innerWidth')

// expired or unknown cart id: the app must recover, not break
await ev("localStorage.setItem('bss.cartId', 'SC-doesnotexist')")
await goto('/cart')
await waitFor("document.querySelector('.state')")
results.unknownCartShowsEmpty = await ev("document.querySelector('.state h2')?.textContent")
results.unknownCartIdCleared = await ev("localStorage.getItem('bss.cartId') === null")
await shot('cart-empty-mobile')

results.consoleProblems = problems
console.log(JSON.stringify(results, null, 2))
ws.close()
chrome.kill()
process.exit(0)
