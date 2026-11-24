import os,asyncio
AQUI=os.path.dirname(os.path.abspath(__file__))
__file__=os.path.join(AQUI,'busca_caminhao.py')
exec(open(__file__,encoding='utf-8').read().split('async def main():')[0])
D='/tmp/mrtruck-testes/sugestoes';os.makedirs(D,exist_ok=True)
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch()
        pg,errs=await setup(b,{'width':1200,'height':900})
        async def os_(num,servs,pecas):
            await pg.fill('#iNum',num);await pg.fill('#iCliente','Transportes Boa Viagem');await pg.fill('#veis [data-k=placa]','RTV4C21')
            for i,(d,v) in enumerate(servs):
                await pg.fill(f'.ld[data-l=servico][data-i="{i}"]',d);await pg.fill(f'.lv[data-l=servico][data-i="{i}"]',v)
            for i,(d,v) in enumerate(pecas):
                await pg.fill(f'.ld[data-l=pecas][data-i="{i}"]',d);await pg.fill(f'.lv[data-l=pecas][data-i="{i}"]',v)
            await pg.click('[data-act=salvar]');await pg.wait_for_timeout(500);await pg.click('#tNova');await pg.wait_for_timeout(300)
        await os_('1',[('Substituir embreagem','850,00'),('Substituir eixo traseiro','1200,00')],[('Disco de embreagem','1500,00')])
        await os_('2',[('Substituir embreagem','900,00'),('Revisão do motor','600,00')],[('Platô de embreagem','2100,00'),('Óleo do motor','300,00')])
        ld=pg.locator('.ld[data-l=servico][data-i="0"]')
        await ld.press_sequentially('substituir e',delay=30);await pg.wait_for_timeout(200)
        print('serviço "substituir e":',[t.replace(chr(10),' ') for t in await pg.locator('#sugL .sli').all_inner_texts()])
        await pg.screenshot(path=f'{D}/servico.png',clip={'x':180,'y':560,'width':840,'height':360})
        await pg.locator('#sugL .sli').first.click();await pg.wait_for_timeout(200)
        print('escolheu:',await ld.input_value(),'| valor:',await pg.input_value('.lv[data-l=servico][data-i="0"]'),'| foco foi pra linha:',await pg.evaluate("document.activeElement.dataset.i"))
        l1=pg.locator('.ld[data-l=servico][data-i="1"]');await l1.press_sequentially('m',delay=30);await pg.wait_for_timeout(200)
        print('serviço "m":',[t.replace(chr(10),' ') for t in await pg.locator('#sugL .sli').all_inner_texts()])
        await pg.keyboard.press('ArrowDown');await pg.keyboard.press('Enter');await pg.wait_for_timeout(200)
        print('teclado escolheu:',await l1.input_value())
        pc=pg.locator('.ld[data-l=pecas][data-i="0"]');await pc.press_sequentially('e',delay=30);await pg.wait_for_timeout(200)
        print('peças "e":',[t.replace(chr(10),' ') for t in await pg.locator('#sugL .sli').all_inner_texts()])
        await pg.keyboard.press('Escape');await pg.wait_for_timeout(100);print('esc fecha:',await pg.locator('#sugL').count()==0)
        print('errs',errs);await b.close()
asyncio.run(main())
