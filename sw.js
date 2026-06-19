/* OBVIOUS · Ring Sizer — service worker */
const VERSION = 'obvious-v7.0.0';
const SHELL = [
  './',
  './index.html',
  './manifest.webmanifest',
  './icon.svg',
  './icon-192.png',
  './icon-512.png',
  './assets/ring-cutout.png',
  './og-image.png'
];
const CDN = ['fonts.googleapis.com','fonts.gstatic.com','cdn.jsdelivr.net','storage.googleapis.com'];

self.addEventListener('install', e => {
  e.waitUntil(
    caches.open(VERSION).then(c => c.addAll(SHELL)).then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', e => {
  e.waitUntil(
    caches.keys().then(keys => Promise.all(
      keys.filter(k => k !== VERSION).map(k => caches.delete(k))
    )).then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', e => {
  const req = e.request;
  if (req.method !== 'GET') return;
  const url = new URL(req.url);

  // navegação: rede primeiro, cai para o app em cache (offline)
  if (req.mode === 'navigate') {
    e.respondWith(
      fetch(req).catch(() => caches.match('./index.html'))
    );
    return;
  }

  // Google Fonts + MediaPipe CDN (WASM/model): stale-while-revalidate → works offline after first use
  if (CDN.some(h => url.hostname.includes(h))) {
    e.respondWith(
      caches.open(VERSION + '-cdn').then(async cache => {
        const hit = await cache.match(req);
        const net = fetch(req).then(res => { if (res && res.ok) cache.put(req, res.clone()); return res; }).catch(() => hit);
        return hit || net;
      })
    );
    return;
  }

  // mesmo domínio: cache primeiro
  if (url.origin === location.origin) {
    e.respondWith(
      caches.match(req).then(hit => hit || fetch(req).then(res => {
        const copy = res.clone();
        caches.open(VERSION).then(c => c.put(req, copy));
        return res;
      }).catch(() => hit))
    );
  }
});
