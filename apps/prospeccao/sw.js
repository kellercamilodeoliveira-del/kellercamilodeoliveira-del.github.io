// Prospecção Keller IA — abre rápido e pega sempre a versão nova quando há internet
const PREFIXO='prospeccao-';
const VERSAO=PREFIXO+'v2';
const ARQUIVOS=['./','./index.html','./manifest.json','./icone-192.png','./icone-512.png','./icone-180.png'];
self.addEventListener('install',e=>{e.waitUntil(caches.open(VERSAO).then(c=>c.addAll(ARQUIVOS)).then(()=>self.skipWaiting()));});
self.addEventListener('activate',e=>{e.waitUntil((async()=>{for(const k of await caches.keys())if(k.startsWith(PREFIXO)&&k!==VERSAO)await caches.delete(k);await self.clients.claim();})());});
self.addEventListener('fetch',e=>{
  const req=e.request;if(req.method!=='GET')return;
  const url=new URL(req.url);
  if(req.mode==='navigate'){e.respondWith(fetch(req).then(r=>{const cp=r.clone();caches.open(VERSAO).then(c=>c.put('./index.html',cp));return r;}).catch(()=>caches.match('./index.html')));return;}
  if(url.origin!==location.origin)return; // Firebase e fontes vão direto
  if(url.pathname.endsWith('leads.json'))return; // lista sempre da internet
  e.respondWith(caches.match(req).then(r=>r||fetch(req)));
});
