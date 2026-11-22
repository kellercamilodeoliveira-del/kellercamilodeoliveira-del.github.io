import os
AQUI=os.path.dirname(os.path.abspath(__file__))
BASE=os.environ.get('BASE','http://localhost:8765/apps/')
FICHAS=os.environ.get('FICHAS','mrtruck-teste')
ESTOQUE=os.environ.get('ESTOQUE','mrtruck-estoque-teste')
os.makedirs('/tmp/mrtruck-testes',exist_ok=True)
import asyncio, os
from playwright.async_api import async_playwright
FAKE = open(os.path.join(AQUI,'fakefb.js')).read()
D='/tmp/mrtruck-testes/os_numero_orcamento'
os.makedirs(D, exist_ok=True)
URL = BASE+FICHAS+'/'

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        ctx = await b.new_context(viewport={'width': 1200, 'height': 900}, service_workers='block')
        await ctx.route('**/firebasejs/**', lambda r: r.fulfill(status=200, content_type='application/javascript', body=FAKE))
        await ctx.add_init_script("document.addEventListener('DOMContentLoaded',()=>{const s=document.createElement('style');s.textContent='#instalar{display:none!important}';document.head.appendChild(s);});")
        pg = await ctx.new_page(); errs = []
        pg.on('pageerror', lambda e: errs.append(str(e)))
        async def login(e, s):
            await pg.wait_for_selector('#lEmail'); await pg.fill('#lEmail', e); await pg.fill('#lSenha', s); await pg.click('#lBtn'); await pg.wait_for_timeout(700)
        await pg.goto(URL)
        await login('admin@teste', '123456'); await pg.click('[data-act=novaOficina]')
        await pg.fill('#fOficina [name=email]', 'dono@teste'); await pg.fill('#fOficina [name=senha]', '123456'); await pg.select_option('#fOficina [name=status]', 'ativo')
        await pg.click('#oBtn'); await pg.wait_for_timeout(500); await pg.click('#modal [data-act=fechar]'); await pg.click('.mtop [data-act=sair]'); await pg.wait_for_timeout(400)
        await login('dono@teste', '123456')

        async def ficha(num, cli='Transportes Teste', placa='ABC1D23'):
            if num is not None: await pg.fill('#iNum', num)
            await pg.fill('#iCliente', cli); await pg.fill('#veis [data-k=placa]', placa)
            await pg.fill('.ld[data-l=servico][data-i="0"]', 'Troca de óleo'); await pg.fill('.lv[data-l=servico][data-i="0"]', '350')
            await pg.click('#iCliente')
        async def erro():
            return (await pg.inner_text('#erro')) if await pg.locator('#erro').count() else ''

        print('hint inicial:', await pg.inner_text('.hnum small'))
        await ficha('5'); await pg.click('[data-act=salvar]'); await pg.wait_for_timeout(500)
        print('salvou 5:', await pg.locator('.ok').count())
        await pg.click('[data-act=nova]'); await pg.wait_for_timeout(300)
        print('hint depois de 5:', await pg.inner_text('.hnum small'))
        for n in ['5', '10', '4']:
            await ficha(n); await pg.click('[data-act=salvar]'); await pg.wait_for_timeout(300)
            print(f'tentou {n}:', await erro())
        await ficha('6'); await pg.click('[data-act=salvar]'); await pg.wait_for_timeout(500)
        print('salvou 6:', await pg.locator('.ok').count())

        # orçamento
        await pg.click('#tOrc'); await pg.wait_for_timeout(300)
        print('orc tem nº?', await pg.locator('#iNum').count(), '| titulo:', await pg.inner_text('.hnum .pre'))
        await ficha(None, 'Rodoviário Orçamento', 'XYZ9K88')
        await pg.fill('.ld[data-l=pecas][data-i="0"]', 'Filtro'); await pg.fill('.lv[data-l=pecas][data-i="0"]', '120'); await pg.click('#iCliente')
        await pg.screenshot(path=f'{D}/1_orc_form.png', full_page=True)
        await pg.click('[data-act=salvar]'); await pg.wait_for_timeout(600)
        print('orc salvo:', await pg.locator('.ok').count(), await pg.locator('[data-act=virarOS]').count())
        await pg.screenshot(path=f'{D}/2_orc_ver.png', full_page=True)
        await pg.click('#tSalvas'); await pg.wait_for_timeout(400)
        print('lista tem orc:', await pg.locator('[data-act=verOrc]').count())
        await pg.screenshot(path=f'{D}/3_lista.png', full_page=True)
        # virar OS
        await pg.click('[data-act=verOrc]'); await pg.wait_for_timeout(300)
        await pg.click('[data-act=virarOS]'); await pg.wait_for_timeout(500)
        print('virar: cliente=', await pg.input_value('#iCliente'), 'linha=', await pg.input_value('.ld[data-l=pecas][data-i="0"]'))
        await pg.fill('#iNum', '7'); await pg.click('[data-act=salvar]'); await pg.wait_for_timeout(600)
        print('OS 7 salva:', await pg.locator('.ok').count())
        # apagar a 7 e tentar 7 de novo
        await pg.click('[data-act=apagar]'); await pg.click('[data-act=apagarOk]'); await pg.wait_for_timeout(400)
        await pg.click('#tNova'); await pg.wait_for_timeout(300)
        print('hint apos apagar 7:', await pg.inner_text('.hnum small'))
        await ficha('7'); await pg.click('[data-act=salvar]'); await pg.wait_for_timeout(300)
        print('tentou 7 de novo:', await erro())
        # troca de aba preserva digitação
        await pg.fill('#iMotorista', 'Zé da OS'); await pg.click('#tOrc'); await pg.wait_for_timeout(200)
        await pg.click('#tNova'); await pg.wait_for_timeout(200)
        print('motorista preservado:', await pg.input_value('#iMotorista'))
        print('errs', errs)
        await b.close()

asyncio.run(main())
