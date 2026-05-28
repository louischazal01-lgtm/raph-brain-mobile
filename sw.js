const CACHE = 'raph-brain-v2';
const SHELL = ['./index.html', './manifest.json'];

self.addEventListener('install', e => {
  e.waitUntil(caches.open(CACHE).then(c => c.addAll(SHELL)));
  self.skipWaiting();
});

self.addEventListener('activate', e => {
  e.waitUntil(
    caches.keys().then(keys =>
      Promise.all(keys.filter(k => k !== CACHE).map(k => caches.delete(k)))
    )
  );
  self.clients.claim();
});

self.addEventListener('fetch', e => {
  // Never intercept API calls — let the browser handle them directly
  if (e.request.url.includes('raphbrain.duckdns.org')) return;

  // Cache-first for static shell assets only
  e.respondWith(
    caches.match(e.request).then(hit => hit || fetch(e.request))
  );
});
