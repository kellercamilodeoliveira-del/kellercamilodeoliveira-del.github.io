import os
AQUI=os.path.dirname(os.path.abspath(__file__))
BASE=os.environ.get('BASE','http://localhost:8765/apps/')
FICHAS=os.environ.get('FICHAS','mrtruck-teste')
ESTOQUE=os.environ.get('ESTOQUE','mrtruck-estoque-teste')
os.makedirs('/tmp/mrtruck-testes',exist_ok=True)
import asyncio, os
from playwright.async_api import async_playwright
FAKE=open(os.path.join(AQUI,'fakefb.js')).read(); D='/tmp/mrtruck-testes/lembretes'; os.makedirs(D,exist_ok=True)
URL=BASE+FICHAS+'/'
HIDE="document.addEventListener('DOMContentLoaded',()=>{const s=document.createElement('style');s.textContent='#instalar{display:none!important}';document.head.appendChild(s);});"
async def setup(b,vp,scale=1,mob=False):
    ctx=await b.new_context(viewport=vp,device_scale_factor=scale,service_workers='block',is_mobile=mob)
    await ctx.add_init_script(HIDE)
    await ctx.route('**/firebasejs/**',lambda r:r.fulfill(status=200,content_type='application/javascript',body=FAKE))
    pg=await ctx.new_page(); errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
    async def login(e,s):
        await pg.wait_for_selector('#lEmail');await pg.fill('#lEmail',e);await pg.fill('#lSenha',s);await pg.click('#lBtn');await pg.wait_for_timeout(700)
    await pg.goto(URL); await login('admin@teste','123456'); await pg.click('[data-act=novaOficina]')
    await pg.fill('#fOficina [name=email]','dono@teste');await pg.fill('#fOficina [name=senha]','123456');await pg.select_option('#fOficina [name=status]','ativo')
    await pg.click('#oBtn');await pg.wait_for_timeout(500);await pg.click('#modal [data-act=fechar]');await pg.click('.mtop [data-act=sair]');await pg.wait_for_timeout(400)
    await login('dono@teste','123456'); return pg,errs
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch()
        pg,errs=await setup(b,{'width':1200,'height':900})
        async def os_(num,km,lemb):
            await pg.fill('#iNum',num);await pg.fill('#iCliente','Transportes Boa Viagem');await pg.fill('#veis [data-k=placa]','RTV4C21')
            await pg.fill('#veis [data-k=modelo]','Volvo FH 540');await pg.fill('#veis [data-k=chassi]','9BVRG40D5LE868123');await pg.fill('#veis [data-k=km]',km)
            await pg.fill('.ld[data-l=servico][data-i="0"]','Serviço teste');await pg.fill('#iLemb',lemb);await pg.click('[data-act=salvar]');await pg.wait_for_timeout(500)
        await os_('1','120000','Motor feito')
        await pg.click('#tNova');await pg.wait_for_timeout(300)
        await os_('2','200000','Embreagem trocada')
        await pg.click('#tNova');await pg.wait_for_timeout(300)
        await pg.fill('#veis [data-k=placa]','RTV4C21');await pg.wait_for_timeout(300)
        print('hint:',(await pg.inner_text('.histbox')).replace('\n',' | '))
        await pg.click('#tLemb');await pg.wait_for_timeout(300)
        print('lista inicial:',(await pg.inner_text('#listaLemb')).replace('\n',' | '))
        await pg.fill('#buscaLemb','868123');await pg.wait_for_timeout(200)
        print('busca chassi:',await pg.locator('#listaLemb [data-act=lembCam]').count())
        await pg.click('#listaLemb [data-act=lembCam]');await pg.wait_for_timeout(300)
        await pg.fill('#lItem','Câmbio revisado');await pg.fill('#lKm','80000');await pg.fill('#lData','2022-05-10');await pg.click('[data-act=lembAdd]');await pg.wait_for_timeout(400)
        print('itens:',[t.replace('\n',' ') for t in await pg.locator('.lit').all_inner_texts()])
        await pg.screenshot(path=f'{D}/lembcam.png',full_page=True)
        await pg.locator('[data-act=lembDel]').last.click();await pg.click('[data-act=lembDelOk]');await pg.wait_for_timeout(300)
        print('apos apagar:',await pg.locator('.lit').count())
        print('errs',errs)
        pg2,e2=await setup(b,{'width':375,'height':700},2,True)
        await pg2.screenshot(path=f'{D}/mob.png')
        print('errs mob',e2)
        await b.close()
asyncio.run(main())
