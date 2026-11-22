import os
AQUI=os.path.dirname(os.path.abspath(__file__))
BASE=os.environ.get('BASE','http://localhost:8765/apps/')
FICHAS=os.environ.get('FICHAS','mrtruck-teste')
ESTOQUE=os.environ.get('ESTOQUE','mrtruck-estoque-teste')
os.makedirs('/tmp/mrtruck-testes',exist_ok=True)
import asyncio, os
from playwright.async_api import async_playwright
FAKE=open(os.path.join(AQUI,'fakefb2.js')).read(); D='/tmp/mrtruck-testes/estoque_integrado'; os.makedirs(D,exist_ok=True)

HIDE="document.addEventListener('DOMContentLoaded',()=>{const s=document.createElement('style');s.textContent='#instalar{display:none!important}';document.head.appendChild(s);});"
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch()
        ctx=await b.new_context(viewport={'width':1100,'height':900},service_workers='block')
        await ctx.add_init_script(HIDE)
        await ctx.route('**/firebasejs/**',lambda r:r.fulfill(status=200,content_type='application/javascript',body=FAKE))
        os_=await ctx.new_page(); errs=[]; os_.on('pageerror',lambda e:errs.append('OS:'+str(e)))
        await os_.goto(BASE+FICHAS+'/'); await os_.evaluate("localStorage.removeItem('__fbdb')"); await os_.reload()
        async def login(pg,e,s):
            await pg.wait_for_selector('#lEmail');await pg.fill('#lEmail',e);await pg.fill('#lSenha',s);await pg.click('#lBtn');await pg.wait_for_timeout(700)
        await login(os_,'admin@teste','123456'); await os_.click('[data-act=novaOficina]')
        await os_.fill('#fOficina [name=email]','dono@teste');await os_.fill('#fOficina [name=senha]','123456');await os_.select_option('#fOficina [name=status]','ativo')
        await os_.click('#oBtn');await os_.wait_for_timeout(500);await os_.click('#modal [data-act=fechar]')
        print('painel tem botão estoque:',await os_.locator('[data-act=estOficina]').count())
        await os_.click('[data-act=estOficina]');await os_.wait_for_timeout(300)  # libera (nova oficina vem bloqueada)
        await os_.click('.mtop [data-act=sair]');await os_.wait_for_timeout(400)
        await login(os_,'dono@teste','123456')
        # estoque app
        es=await ctx.new_page(); es.on('pageerror',lambda e:errs.append('EST:'+str(e)))
        await es.goto(BASE+ESTOQUE+'/'); await es.wait_for_timeout(1200)
        print('estoque abriu:',await es.locator('[data-act=novoProd]').count())
        print('tem botao de saida?',await es.locator('.menos,[data-t=saida]').count(),'| link fichas?',await es.locator('a[href*=mrtruck]').count())
        for cod,nome,qtd,mini,maxi,preco in [('15',"Bomba d'água",'3','2','10','450'),('22','Filtro de óleo','10','4','20','45,90')]:
            await es.click('#tNovo');await es.wait_for_timeout(200)
            await es.fill('#pCod',cod);await es.fill('#pNome',nome);await es.fill('#pQtd',qtd);await es.fill('#pMin',mini);await es.fill('#pMax',maxi);await es.fill('#pPreco',preco)
            await es.click('[data-act=salvarProd]');await es.wait_for_timeout(300)
        await es.click('#tEst');await es.wait_for_timeout(300)
        print('lista:',[t.replace('\n',' ') for t in await es.locator('.prod').all_inner_texts()])
        # código duplicado
        await es.click('#tNovo');await es.fill('#pCod','15');await es.fill('#pNome','Outra');await es.click('[data-act=salvarProd]');await es.wait_for_timeout(200)
        print('dup:',await es.inner_text('#erro'))
        # OS app picks products
        await os_.bring_to_front();await os_.wait_for_timeout(1500)
        await os_.click('#tNova');await os_.wait_for_timeout(300)
        print('dica aparece:',await os_.locator('.dica').count())
        await os_.fill('#iNum','100');await os_.fill('#iCliente','Transportes Boa Viagem');await os_.fill('#veis [data-k=placa]','RTV4C21')
        await os_.fill('.ld[data-l=servico][data-i="0"]','Troca da bomba d\'água')
        await os_.fill('.ld[data-l=pecas][data-i="0"]','15');await os_.press('.ld[data-l=pecas][data-i="0"]','Enter');await os_.wait_for_timeout(200)
        await os_.fill('.ld[data-l=pecas][data-i="1"]','2x22');await os_.press('.ld[data-l=pecas][data-i="1"]','Enter');await os_.wait_for_timeout(200)
        await os_.fill('.ld[data-l=pecas][data-i="2"]','Abraçadeira comum');await os_.fill('.lv[data-l=pecas][data-i="2"]','12')
        vals=[(await os_.input_value(f'.ld[data-l=pecas][data-i="{i}"]'),await os_.input_value(f'.lv[data-l=pecas][data-i="{i}"]')) for i in range(3)]
        print('linhas peças:',vals,'| chips:',await os_.locator('.pcod').all_inner_texts())
        await os_.screenshot(path=f'{D}/ficha.png',full_page=True)
        await os_.click('[data-act=salvar]');await os_.wait_for_timeout(500)
        await os_.click('[data-act=finalizar]');await os_.wait_for_timeout(300)
        print('modal baixa:',(await os_.inner_text('.baixa')).replace('\n',' | '))
        await os_.screenshot(path=f'{D}/finalizar.png')
        await os_.click('[data-act=finalizarOk]');await os_.wait_for_timeout(600)
        print('toast:',await os_.inner_text('#toast'))
        print('aviso minimo na OS:',(await os_.inner_text('#modal')).replace('\n',' | ') if await os_.locator('#modal.show').count() else 'NENHUM')
        await os_.screenshot(path=f'{D}/os_minimo.png')
        if await os_.locator('#modal.show').count(): await os_.click('#modal [data-act=fechar]')
        # estoque reflects
        await es.bring_to_front();await es.wait_for_timeout(1500)
        await es.click('#tEst');await es.wait_for_timeout(300)
        print('estoque depois:',[t.replace('\n',' ') for t in await es.locator('.prod').all_inner_texts()])
        print('faixa:',(await es.inner_text('.faixa')).replace('\n',' | ') if await es.locator('.faixa').count() else 'sem faixa')
        await es.screenshot(path=f'{D}/estoque_alerta.png',full_page=True)
        await es.click('#tMovs');await es.wait_for_timeout(300)
        print('alertas:',[t.replace('\n',' ') for t in await es.locator('.prod').all_inner_texts()])
        await es.screenshot(path=f'{D}/alertas.png',full_page=True)
        # reabrir o app de estoque: aviso ao abrir
        es2=await ctx.new_page();await es2.goto(BASE+ESTOQUE+'/');await es2.wait_for_timeout(1500)
        print('aviso ao abrir:',(await es2.inner_text('#modal')).replace('\n',' | ') if await es2.locator('#modal.show').count() else 'NENHUM')
        await es2.set_viewport_size({'width':390,'height':844});await es2.screenshot(path=f'{D}/abrir_aviso.png');await es2.close()
        # reabrir → estorno
        await os_.bring_to_front();await os_.click('[data-act=reabrir]');await os_.wait_for_timeout(600)
        await es.bring_to_front();await es.wait_for_timeout(1500);await es.click('#tEst');await es.wait_for_timeout(300)
        print('estoque apos reabrir:',[t.replace('\n',' ') for t in await es.locator('.prod').all_inner_texts()])
        # entrada manual
        await es.locator('.prod .mais').first.click();print('modal entrada:',(await es.inner_text('#modal')).replace('\n',' | ')[:200]);await es.fill('#mQ','9');await es.fill('#mObs','Nota 123');await es.click('[data-act=movOk]');await es.wait_for_timeout(300)
        print('apos entrada:',(await es.locator('.prod').first.inner_text()).replace('\n',' '))
        await es.screenshot(path=f'{D}/estoque.png',full_page=True)
        print('errs',errs)
        await b.close()
asyncio.run(main())
