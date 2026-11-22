import os
AQUI=os.path.dirname(os.path.abspath(__file__))
BASE=os.environ.get('BASE','http://localhost:8765/apps/')
FICHAS=os.environ.get('FICHAS','mrtruck-teste')
ESTOQUE=os.environ.get('ESTOQUE','mrtruck-estoque-teste')
os.makedirs('/tmp/mrtruck-testes',exist_ok=True)
import asyncio
from playwright.async_api import async_playwright
FAKE=open(os.path.join(AQUI,'fakefb2.js')).read()
TRAVA=FAKE.replace("export const onAuthStateChanged=(a,cb)=>{","export const onAuthStateChanged=(a,cb)=>{return()=>{};")
HANG="indexedDB.open=function(){return {};};"  # nunca responde
async def run(app,fake,hang,espera,nome):
  async with async_playwright() as p:
    b=await p.chromium.launch();ctx=await b.new_context(viewport={'width':390,'height':844})
    await ctx.route('**/firebasejs/**',lambda r:r.fulfill(status=200,content_type='application/javascript',body=fake))
    await ctx.add_init_script("window.addEventListener('DOMContentLoaded',()=>{const s=document.createElement('style');s.textContent='#instalar{display:none!important}';document.head.appendChild(s)});"+(HANG if hang else ''))
    pg=await ctx.new_page();errs=[];pg.on('pageerror',lambda e:errs.append(str(e)))
    await pg.goto(f'{BASE}{app}/');await pg.wait_for_timeout(espera)
    txt=(await pg.inner_text('#app'))[:160].replace('\n',' | ')
    await pg.screenshot(path=f'/tmp/mrtruck-testes/{nome}.png');print(nome,'->',txt,'errs',errs);await b.close()
async def main():
  for app in [FICHAS,ESTOQUE]:
    await run(app,FAKE,True,3500,app+'_idbtrava')      # banco local travado: tem que abrir mesmo assim
    await run(app,TRAVA,False,11500,app+'_demora')     # nada responde: aparece a ajuda
asyncio.run(main())
