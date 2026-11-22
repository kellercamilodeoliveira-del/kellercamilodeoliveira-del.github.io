// Firebase de mentira, só para testar a tela (memória + regras simplificadas)
const G=globalThis.__fb||(globalThis.__fb={users:{'admin@teste':{uid:'ADM',senha:'123456'}},docs:{},cur:null,authCbs:[],snaps:[],n:0});
const ADMIN='admin@teste';
const err=c=>{const e=new Error(c);e.code=c;return e;};
export const initializeApp=(c,name)=>({name:name||'def'});
export const deleteApp=async()=>{};
const auths={};
export const getAuth=app=>auths[app.name]||(auths[app.name]={app,currentUser:app.name==='def'?G.cur:null});
const fire=()=>{const a=auths.def;a.currentUser=G.cur;G.authCbs.forEach(cb=>cb(G.cur));};
export const onAuthStateChanged=(a,cb)=>{G.authCbs.push(cb);setTimeout(()=>cb(G.cur),10);return()=>{};};
const mkUser=(email)=>({uid:G.users[email].uid,email,emailVerified:true,reload:async()=>{},getIdToken:async()=>''});
export const signInWithEmailAndPassword=async(a,email,senha)=>{const u=G.users[email];if(!u||u.senha!==senha)throw err('auth/invalid-credential');
  if(a.app.name==='def'){G.cur=mkUser(email);fire();}else a.currentUser=mkUser(email);return{user:mkUser(email)};};
export const createUserWithEmailAndPassword=async(a,email,senha)=>{if(G.users[email])throw err('auth/email-already-in-use');G.users[email]={uid:'U'+(++G.n),senha};
  const u=mkUser(email);if(a.app.name==='def'){G.cur=u;fire();}else a.currentUser=u;return{user:u};};
export const signOut=async a=>{if(a.app.name==='def'){G.cur=null;fire();}else a.currentUser=null;};
export const sendPasswordResetEmail=async()=>{};
export const sendEmailVerification=async()=>{};
// firestore
export const persistentLocalCache=()=>({});export const persistentMultipleTabManager=()=>({});
export const initializeFirestore=()=>({});
export const collection=(db,...p)=>({kind:'col',path:p.join('/')});
export const doc=(db,...p)=>({kind:'doc',path:p.join('/'),id:p[p.length-1]});
export const serverTimestamp=()=>({__ts:Date.now()});
export class Timestamp{constructor(ms){this.ms=ms;}toMillis(){return this.ms;}static fromDate(d){return new Timestamp(+d);}}
const isAdmin=()=>G.cur&&G.cur.email===ADMIN;
const perfil=()=>G.cur&&G.docs['os_usuarios/'+G.cur.uid];
function pode(path,op){
  if(!G.cur)return false;if(isAdmin())return true;
  const p=path.split('/');
  if(p[0]==='os_usuarios')return op==='get'&&p[1]===G.cur.uid;
  if(p[0]==='os_oficinas'){const pf=perfil();if(!pf||pf.oficinaId!==p[1])return false;
    if(op==='get'||op==='list')return p.length>1;
    const of=G.docs['os_oficinas/'+p[1]];const lib=of&&(of.status==='ativo'||(of.status==='teste'&&of.fimTeste.toMillis()>Date.now()));
    if(p.length===2)return lib&&op==='update';return lib;}
  return false;}
const notify=()=>setTimeout(()=>G.snaps.forEach(s=>s()),0);
const snapDoc=path=>({exists:()=>!!G.docs[path],data:()=>G.docs[path]&&JSON.parse(JSON.stringify(G.docs[path]),rev),id:path.split('/').pop()});
const rev=(k,v)=>v&&v.ms!==undefined&&Object.keys(v).length===1?new Timestamp(v.ms):v;
const snapCol=path=>{const pre=path+'/';const ids=Object.keys(G.docs).filter(k=>k.startsWith(pre)&&!k.slice(pre.length).includes('/'));return{docs:ids.map(k=>snapDoc(k))};};
export const getDoc=async r=>{if(!pode(r.path,'get'))throw err('permission-denied');return snapDoc(r.path);};
export const setDoc=async(r,d)=>{if(!pode(r.path,G.docs[r.path]?'update':'create'))throw err('permission-denied');G.docs[r.path]=JSON.parse(JSON.stringify(d));notify();};
export const updateDoc=async(r,d)=>{if(!pode(r.path,'update'))throw err('permission-denied');if(!isAdmin()&&Object.keys(d).some(k=>['status','fimTeste','donoUid','email'].includes(k)))throw err('permission-denied');G.docs[r.path]={...G.docs[r.path],...JSON.parse(JSON.stringify(d))};notify();};
export const deleteDoc=async r=>{if(!pode(r.path,'delete'))throw err('permission-denied');delete G.docs[r.path];notify();};
export const writeBatch=()=>{const ops=[];return{set:(r,d)=>ops.push([r,d]),commit:async()=>{for(const[r,d]of ops)await setDoc(r,d);}};};
export const onSnapshot=(r,ok,bad)=>{
  const op=r.kind==='col'?'list':'get';
  if(r.kind==='col'&&r.path==='os_oficinas'&&!isAdmin()){setTimeout(()=>bad&&bad(err('permission-denied')),5);return()=>{};}
  if(!pode(r.path,op)){setTimeout(()=>bad&&bad(err('permission-denied')),5);return()=>{};}
  const f=()=>ok(r.kind==='col'?snapCol(r.path):snapDoc(r.path));G.snaps.push(f);setTimeout(f,5);return()=>{G.snaps=G.snaps.filter(x=>x!==f);};};
export const initializeAuth=(app,o)=>getAuth(app);export const indexedDBLocalPersistence={};export const browserLocalPersistence={};export const inMemoryPersistence={};export const memoryLocalCache=()=>({});
