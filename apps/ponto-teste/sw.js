// Service worker: guarda o app no celular para abrir sem internet
const PREFIXO='ponto-teste-';
const VERSAO=PREFIXO+'v9';
const FB='https://www.gstatic.com/firebasejs/10.12.2/';
const JSPDF='https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.5.1/jspdf.umd.min.js';
const LOCAIS=['./','./index.html','./manifest.webmanifest','./icons/icon-192.png','./icons/icon-512.png','./icons/icon-maskable-512.png','./icons/apple-touch-icon.png','../../fonts/inter-400.woff2','../../fonts/inter-500.woff2','../../fonts/inter-600.woff2'];
const EXTERNOS=[JSPDF,FB+'firebase-app.js',FB+'firebase-auth.js',FB+'firebase-firestore.js'];
const guardavel=u=>u.startsWith(self.location.origin)||u===JSPDF||u.startsWith(FB)||u.startsWith('https://fonts.');

self.addEventListener('install',e=>{
  e.waitUntil((async()=>{
    const c=await caches.open(VERSAO);
    for(const u of LOCAIS){try{await c.add(u)}catch(err){}}
    for(const u of EXTERNOS){try{const r=await fetch(u,{mode:'cors'});if(r.ok)await c.put(u,r)}catch(err){}}
    self.skipWaiting();
  })());
});
self.addEventListener('activate',e=>{
  e.waitUntil((async()=>{
    for(const k of await caches.keys())if(k.startsWith(PREFIXO)&&k!==VERSAO)await caches.delete(k); // só apaga o cache deste app
    await self.clients.claim();
  })());
});
self.addEventListener('fetch',e=>{
  const req=e.request;if(req.method!=='GET')return;
  if(req.mode==='navigate'){
    e.respondWith(fetch(req).then(r=>{const cp=r.clone();caches.open(VERSAO).then(c=>c.put('./index.html',cp));return r}).catch(()=>caches.match('./index.html')));
    return;
  }
  if(!guardavel(req.url))return; // conexões do Firebase passam direto
  e.respondWith(caches.match(req).then(hit=>hit||fetch(req).then(r=>{
    if(r.ok){const cp=r.clone();caches.open(VERSAO).then(c=>c.put(req,cp))}
    return r;
  })));
});
