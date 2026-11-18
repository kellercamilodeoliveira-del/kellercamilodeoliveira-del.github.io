// MR Truck — Fichas: funciona sem internet depois de aberto uma vez
const PREFIXO='mrtruck-';
const VERSAO=PREFIXO+'v14';
const ARQUIVOS=['./','./index.html','./manifest.json','./logo-mrtruck.svg','./icone-192.png','./icone-512.png','./icone-180.png'];
self.addEventListener('install',e=>{e.waitUntil(caches.open(VERSAO).then(c=>c.addAll(ARQUIVOS)).then(()=>self.skipWaiting()));});
self.addEventListener('activate',e=>{e.waitUntil((async()=>{for(const k of await caches.keys())if(k.startsWith(PREFIXO)&&k!==VERSAO)await caches.delete(k);await self.clients.claim();})());});
self.addEventListener('fetch',e=>{
  const req=e.request;if(req.method!=='GET')return;
  if(req.mode==='navigate'){ // sempre tenta a versão nova; sem internet usa a guardada
    e.respondWith(fetch(req).then(r=>{const cp=r.clone();caches.open(VERSAO).then(c=>c.put('./index.html',cp));return r;}).catch(()=>caches.match('./index.html')));return;}
  if(req.url.includes('gstatic.com/firebasejs/')){ // guarda o Firebase para abrir sem internet
    e.respondWith(caches.match(req).then(r=>r||fetch(req).then(res=>{const cp=res.clone();caches.open(VERSAO).then(c=>c.put(req,cp));return res;})));return;}
  if(new URL(req.url).origin!==location.origin)return; // Firebase (dados) vai direto
  e.respondWith(caches.match(req).then(r=>r||fetch(req)));
});
