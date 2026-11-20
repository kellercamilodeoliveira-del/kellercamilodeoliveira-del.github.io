// Painel MR Truck: guarda a moldura do painel para abrir mesmo com a internet oscilando
const C='mrtruck-painel-p1';
self.addEventListener('install',e=>{e.waitUntil(caches.open(C).then(c=>c.addAll(['./','./index.html','./manifest.json'])).then(()=>self.skipWaiting()));});
self.addEventListener('activate',e=>{e.waitUntil((async()=>{for(const k of await caches.keys())if(k.startsWith('mrtruck-painel-')&&k!==C)await caches.delete(k);await self.clients.claim();})());});
self.addEventListener('fetch',e=>{if(e.request.mode!=='navigate')return;
  e.respondWith(fetch(e.request).then(r=>{const cp=r.clone();caches.open(C).then(c=>c.put('./index.html',cp));return r;}).catch(()=>caches.match('./index.html')));});
