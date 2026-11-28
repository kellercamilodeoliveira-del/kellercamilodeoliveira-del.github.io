# Botão "GERAR PDF" na OS e no Orçamento: tem que sair um arquivo .pdf de 1 página A4.
import os,asyncio
AQUI=os.path.dirname(os.path.abspath(__file__))
__file__=os.path.join(AQUI,'busca_caminhao.py')
exec(open(__file__,encoding='utf-8').read().split('async def main():')[0])
D='/tmp/mrtruck-testes/pdf';os.makedirs(D,exist_ok=True)
async def baixa(pg,act,nome):
    async with pg.expect_download(timeout=20000) as dl:
        await pg.click(f'[data-act={act}]')
    d=await dl.value;cam=f'{D}/{nome}';await d.save_as(cam)
    dados=open(cam,'rb').read()
    print(act,'->',d.suggested_filename,'| pdf:',dados[:5]==b'%PDF-','| tamanho ok:',len(dados)>20000,'| A4:',b'/MediaBox [0 0 595.27' in dados)
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch()
        pg,errs=await setup(b,{'width':1200,'height':900})
        await pg.fill('#iNum','77');await pg.fill('#iCliente','José da Silva');await pg.fill('#veis [data-k=placa]','BZF4545')
        await pg.fill('.ld[data-l=servico][data-i="0"]','Troca de embreagem');await pg.fill('.lv[data-l=servico][data-i="0"]','1500')
        await pg.click('[data-act=salvar]');await pg.wait_for_timeout(500)
        print('botão OS:',await pg.inner_text('[data-act=pdf]'))
        await baixa(pg,'pdf','os.pdf')
        await pg.click('#tOrc');await pg.wait_for_timeout(300)
        await pg.wait_for_timeout(300)
        await pg.fill('#iCliente','Rodoviário Silva');await pg.fill('#veis [data-k=placa]','FTR2B88');await pg.fill('.ld[data-l=servico][data-i="0"]','Revisão de freio');await pg.fill('.lv[data-l=servico][data-i="0"]','800');await pg.click('#iCliente')
        await pg.click('[data-act=salvar]');await pg.wait_for_timeout(600)
        await pg.screenshot(path=f'{D}/orc_ver.png',full_page=True)
        print('botão orçamento:',await pg.inner_text('[data-act=pdfOrc]'))
        await baixa(pg,'pdfOrc','orc.pdf')
        print('errs',errs);await b.close()
asyncio.run(main())
