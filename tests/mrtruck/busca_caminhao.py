import os
AQUI=os.path.dirname(os.path.abspath(__file__))
BASE=os.environ.get('BASE','http://localhost:8765/apps/')
FICHAS=os.environ.get('FICHAS','mrtruck-teste')
ESTOQUE=os.environ.get('ESTOQUE','mrtruck-estoque-teste')
os.makedirs('/tmp/mrtruck-testes',exist_ok=True)
import asyncio, os
from playwright.async_api import async_playwright
FAKE=open(os.path.join(AQUI,'fakefb.js')).read(); D='/tmp/mrtruck-testes/busca_caminhao'; os.makedirs(D,exist_ok=True)
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
        txt=lambda sel: pg.inner_text(sel)
        # duas OS antigas, dois caminhões
        async def os_(num,cli,placa,modelo,chassi,km,mot,serv):
            await pg.fill('#iNum',num);await pg.fill('#iCliente',cli);await pg.fill('#iMotorista',mot);await pg.fill('#veis [data-k=placa]',placa)
            await pg.fill('#veis [data-k=modelo]',modelo);await pg.fill('#veis [data-k=chassi]',chassi);await pg.fill('#veis [data-k=km]',km)
            await pg.fill('.ld[data-l=servico][data-i="0"]',serv);await pg.click('[data-act=salvar]');await pg.wait_for_timeout(500)
            await pg.click('#tNova');await pg.wait_for_timeout(300)
        await os_('1','Transportes Boa Viagem','RTV4C21','Volvo FH 540','9BVRG40D5LE868123','120000','Zé Carlos','Troca de embreagem')
        await os_('2','Rodoviário Silva','FTR2B88','Scania R450','9BSR4X200P3912345','310000','Marcão','Revisão de freio')
        # 1) chassi pela metade -> sugestão -> toca -> puxa tudo
        await pg.locator('#veis [data-k=chassi]').press_sequentially('868',delay=40);await pg.wait_for_timeout(200)
        print('sug chassi:',(await txt('.sugbox')).replace('\n',' | '))
        await pg.click('.sugi[data-p=RTV4C21]');await pg.wait_for_timeout(300)
        vals=[await pg.input_value(f'#veis [data-k={k}]') for k in ('placa','modelo','chassi')]
        print('puxou:',vals,'| cliente:',await pg.input_value('#iCliente'),'| motorista:',await pg.input_value('#iMotorista'))
        print('historico:',(await txt('.histbox')).replace('\n',' | '))
        print('cliente hist:',(await txt('#conhecidos')).replace('\n',' | ')[:160])
        await pg.screenshot(path=f'{D}/chassi.png',full_page=True)
        # 2) modelo
        await pg.click('[data-act=limparForm]');await pg.wait_for_timeout(300)
        if await pg.locator('#modal.show').count(): await pg.click('#modal .B')
        await pg.wait_for_timeout(200)
        await pg.locator('#veis [data-k=modelo]').press_sequentially('scania',delay=30);await pg.wait_for_timeout(200)
        print('sug modelo:',(await txt('.sugbox')).replace('\n',' | '))
        await pg.click('.sugi[data-p=FTR2B88]');await pg.wait_for_timeout(300)
        print('puxou modelo:',await pg.input_value('#veis [data-k=placa]'),await pg.input_value('#iCliente'),await pg.input_value('#iMotorista'))
        # 3) placa completa digitada -> preenche sozinho
        await pg.click('[data-act=limparForm]');await pg.wait_for_timeout(300)
        if await pg.locator('#modal.show').count(): await pg.click('#modal .B')
        await pg.wait_for_timeout(200)
        await pg.locator('#veis [data-k=placa]').press_sequentially('RTV4C21',delay=30);await pg.wait_for_timeout(300)
        print('placa auto:',await pg.input_value('#veis [data-k=modelo]'),'|',await pg.input_value('#veis [data-k=chassi]'),'|',await pg.input_value('#iCliente'),'| foco na placa:',await pg.evaluate("document.activeElement.dataset.k"))
        # 4) cliente digitado -> histórico do cliente
        await pg.click('[data-act=limparForm]');await pg.wait_for_timeout(300)
        if await pg.locator('#modal.show').count(): await pg.click('#modal .B')
        await pg.wait_for_timeout(200)
        await pg.locator('#iCliente').press_sequentially('Rodoviário Silva',delay=20);await pg.wait_for_timeout(200)
        print('cliente:',(await txt('#conhecidos')).replace('\n',' | '))
        await pg.screenshot(path=f'{D}/cliente.png',full_page=True)
        # 5) busca de clientes por chassi
        await pg.click('#tSalvas');await pg.wait_for_timeout(300);await pg.fill('#busca','3912');await pg.wait_for_timeout(200)
        print('busca clientes por chassi:',[t.split(chr(10))[0] for t in await pg.locator('#lista .card').all_inner_texts()])
        print('errs',errs)
        await b.close()
asyncio.run(main())
