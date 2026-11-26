# Apps dos clientes (mantidos pelo time de agentes)

Cada app tem duas pastas:
- `apps/<app>/` → versão OFICIAL, a que o cliente usa. Só muda depois que o cliente aprovar o teste.
- `apps/<app>-teste/` → versão de TESTE, onde o agente Mecânico aplica as alterações e manda o link pro cliente conferir.

Regras para o agente Mecânico:
1. Toda alteração começa na pasta `-teste`. Nunca editar a oficial direto.
2. Depois que o cliente aprovar: copiar os arquivos do teste pra oficial, MAS manter na oficial: o nome do banco offline (`indexedDB.open('checklist-frota',1)`), o título sem "TESTE", o manifest sem "TESTE", sem a faixa amarela de teste e o `PREFIXO` do sw.js da oficial. Subir a versão do cache (`VERSAO=PREFIXO+'vN'`) nas duas pastas a cada publicação, pra os celulares pegarem a versão nova.
3. Não mudar a configuração do Firebase, os nomes das coleções do Firestore nem o formato dos dados salvos sem passar pelo Keller (o teste grava no mesmo banco que o oficial).

## Checklist de Frota — Gers Florestal
- Oficial: https://kellercamilodeoliveira-del.github.io/apps/checklist-gers/
- Teste: https://kellercamilodeoliveira-del.github.io/apps/checklist-gers-teste/
- Regra fixa da Bracell/Gers: o cabeçalho dos checklists tem que manter escrito "GERS FLORESTAL" (e "Bracell" nos checklists da Bracell), mesmo com logos.
- Versão antiga ainda no ar (congelada, sem créditos no Netlify): https://checklist-frota-keller.netlify.app

## Ponto Eletrônico (produto Keller IA, multiempresa)
- App: https://kellercamilodeoliveira-del.github.io/apps/ponto/
- Link do funcionário de cada empresa: `.../apps/ponto/?e=<id da empresa>` (aparece no painel do gestor).
- Firebase: projeto `escritorio-c3acb` (compartilhado), coleções `ponto_empresas` e `ponto_usuarios`. As regras desse app estão em `apps/ponto/firestore.rules` e foram somadas às regras do projeto (não substituir as dos outros apps).
- Administrador (master): keller_camilo@hotmail.com ou kellercamilodeoliveira@gmail.com, com e-mail confirmado.
- Teste: https://kellercamilodeoliveira-del.github.io/apps/ponto-teste/ (pasta `apps/ponto-teste/`, mesmo banco do oficial).
  Ao publicar o teste na oficial, manter na oficial: título sem "TESTE", sem a faixa amarela, manifest sem TESTE e `PREFIXO='ponto-oficial-'` no sw.js; subir a VERSAO nas duas.
- O app é um só para todas as empresas. Personalização de UMA empresa (logo, cor) vai no mapa `MARCAS` do index.html (chave = id da empresa) e no mapa `MARCAS` do `ponto.js` do motor, ou pela aba Empresa > Marca do próprio painel. Não fazer mudança que afete as outras empresas sem passar pelo Keller.
- Comprovante por WhatsApp: rota `/ponto/comprovante` do motor (repositório motor-whatsapp-keller-ia, arquivo ponto.js).
- Regras do Firestore do Ponto: `apps/ponto/firestore.rules` (só o Keller publica no Firebase; mudança de regra = escalar).
- Clientes: Betolub Serviços Automotivos (empresa `betolubservicosa-cmcx`), WhatsApp (14) 99119-9934 e (14) 99111-2441 (Fernando).
- Cadastro do colaborador: nome completo, CPF (campo `cpf`, formato 000.000.000-00; cadastros antigos podem ter `rg`) e WhatsApp com DDD.
- Jornada padrão por empresa: mapa `JORNADA_EMPRESA` no index.html (vale até o gestor salvar outra na aba Empresa). Betolub: seg–sex 08:30–12:00 e 13:30–18:00 (8h), sáb 08:00–13:00 (5h).
- Modo tablet (`?e=<empresa>&tablet=1`): só a tela de bater ponto, sem botão "Área do gestor". Para tirar um aparelho do modo tablet: abrir `.../apps/ponto/?tablet=0`.
- Quadro "Horários de hoje" ao lado do teclado (só no modo tablet): batidas feitas naquele tablet, guardadas só no aparelho (localStorage `ponto.quadro.<empresa>`); vermelho = fora da tolerância. Horários e tolerâncias no mapa `HORARIO_EMPRESA` e em `apps/ponto/horarios.json` (o motor lê esse arquivo a cada 10 min — mudar os dois juntos; Betolub: tolerância 10 min, saída do fim do dia 6 min); às 21:00 (`VIRADA_QUADRO`) o quadro passa para o dia seguinte. Avisos de horário no WhatsApp do gestor: `pontoAlertas.js` do motor.
- Painel (gestor e administrador): aba **Banco** = banco de horas acumulado mês a mês + PDF; no Relatório, tocar no dia permite **Editar** a hora de uma batida (guarda `tsOriginal`, `motivoEdicao`, `editado: true`), incluir ou apagar.
- Botão **⟳ Atualizar** no topo do painel e da lista de empresas: limpa o cache do app e recarrega. Quando sai versão nova (sw.js com VERSAO nova), o painel mostra o aviso "Tem versão nova do app" e o tablet recarrega sozinho quando ninguém está digitando.
- Começo da contagem do banco (aba Banco): mapa `INICIO_BANCO_EMPRESA` (Betolub = 2026-11-13, pra não contar os dias de instalação/teste) ou campo `inicioBanco` da empresa; botão "Zerar o banco de todos a partir de hoje". `inicioDe` = maior entre o início do funcionário e o início do banco da empresa.

## DuaPi.NFe — Nota fiscal eletrônica (produto Keller IA, multiempresa)
- App: https://kellercamilodeoliveira-del.github.io/apps/nfe/ (arquivo único `apps/nfe/index.html`).
- Emite NF-e modelo 55 DIRETO na Sefaz (sem Focus NFe nem serviço pago). Quem fala com a Sefaz é o motor (`nfe.js` do repositório motor-whatsapp-keller-ia), rotas `/nfe/...`.
- Empresa é criada pelo Keller no WhatsApp: `#nfe nova Nome` (gera código + senha). `#nfe empresas`, `#nfe senha código`.
- Certificado A1 e dados ficam no Firestore (coleção `config`, docs `nfe-emp-*` e `nfe-xml-*`), criptografados pelo cofre do motor.
- Começa em homologação (teste). Produção só depois de 1 nota de teste autorizada + digitar PRODUCAO.
- Versão 1: só Simples Nacional (CRT 1) e MEI (CRT 4). Regime normal (CRT 3) ainda não.
- Busca de CEP (ViaCEP), CNPJ e NCM (BrasilAPI) direto do navegador.

## MR Truck Service — Fichas (Pré Ordem de Serviço)
- App: https://kellercamilodeoliveira-del.github.io/apps/mrtruck/ (arquivo único `apps/mrtruck/index.html`).
- Cliente: MR Truck Service LTDA - ME (São Manuel-SP), oficina de caminhões Volvo.
- Ficha igual ao talão de papel; cada cliente tem cadastro com vários caminhões (botão "Adicionar mais um caminhão").
- O Nº da ordem de serviço é digitado à mão pelo dono (campo no canto direito da folha), obrigatório e sem repetir. Nada de número automático.
- Instala como aplicativo (PWA) no computador e no Android: botão azul "Instalar no computador" aparece sozinho no Chrome/Edge. Funciona sem internet (`sw.js`, `PREFIXO='mrtruck-'`; subir a VERSAO a cada mudança).
- Dados ficam só no aparelho (localStorage `mrtruck_ficha_papel_v1`), com cópia de segurança em Ajustes. Não mudar essa chave sem passar pelo Keller.

## Painel dos Sistemas (uso do Keller)
- Link: https://kellercamilodeoliveira-del.github.io/apps/painel/ (arquivo único `apps/painel/index.html`).
- Mostra todos os sistemas no ar ao mesmo tempo, em telinhas; clicar numa tela amplia (Esc ou "Voltar ao painel" volta). Bolinha verde = respondeu, vermelha = sem resposta (verifica a cada 1 min).
- Lista padrão no array `PADRAO` do index.html. Sistema novo do Keller → acrescentar lá (entra sozinho no painel dele). Sistema que sair do ar de vez → tirar de lá.
- O que o Keller marca/desmarca, a ordem e os extras ficam só no navegador dele (localStorage `painel-sistemas-keller-v1`).
- Motor do WhatsApp recarrega sozinho a cada 2 min (mantém o Render acordado e o status atualizado).
- DESDE 17/11/2026 o link oficial `apps/mrtruck/` é a versão com LOGIN na nuvem (mesmo código do `mrtruck-teste/`, que fica para testes). Oficina MR Truck cadastrada (`os_oficinas/mr-truck-service-f7ml`, status ativo; login do dono = e-mail do Fernando, que cria a própria senha pelo e-mail de redefinição).
- Versão de teste com LOGIN (modelo do Ponto): https://kellercamilodeoliveira-del.github.io/apps/mrtruck-teste/
  - Firebase `escritorio-c3acb`, coleções `os_oficinas/{oficina}/clientes|fichas` e `os_usuarios/{uid}` ({oficinaId, papel:'dono'}).
  - Administrador = mesma regra `pontoMaster()` do Ponto (o app descobre que é admin porque consegue listar `os_oficinas`; o e-mail não fica no código).
  - Painel do administrador: cadastrar oficina (cria login e senha da oficina), Liberar / Teste 7 dias / Bloquear, Ver fichas, Trocar senha.
  - Regras: `apps/mrtruck-teste/firestore.rules` — PUBLICADAS no Firebase em 16/11/2026, logo depois do bloco do Ponto.
  - Depois das regras publicadas e testado: copiar `mrtruck-teste/index.html` para `mrtruck/` (título sem TESTE, `PREFIXO='mrtruck-'` no sw.js, subir VERSAO). Na primeira entrada da oficina, as fichas guardadas no aparelho sobem sozinhas para a nuvem.
- ATUALIZAÇÃO AUTOMÁTICA (desde 18/11/2026): cada publicação do MR Truck precisa mudar `APP_VERSAO` no index.html E o `version.json` da mesma pasta (mesmo valor do VERSAO do sw.js). O app aberto confere a cada 3 min / ao voltar para a janela e se recarrega sozinho; se houver ficha sendo digitada, espera salvar. Sem mudar o version.json, ninguém recebe a versão nova até fechar e abrir.

## Controle de Estoque (apps/mrtruck-estoque)
- Sistema separado (link e ícone próprios), mesmo login e mesmos dados da oficina no Firebase.
- Produtos: `os_oficinas/{oficina}/estoque_produtos`; movimentos: `os_oficinas/{oficina}/estoque_movs` (quantidade = soma dos movimentos).
- Nas Fichas, a peça com código (ex.: digitar `15` ou `2x15` + Enter) dá baixa no estoque quando a OS é finalizada; reabrir/apagar a OS devolve as peças.
- Liberar/bloquear por oficina: campo `estoque` ('ativo' | 'bloqueado') no painel do administrador. Oficinas novas nascem com o estoque bloqueado; a MR Truck (sem o campo) está liberada.
- Publicar: aumentar `e<N>` em `APP_VERSAO` (index.html), `VERSAO` (sw.js) e `version.json`.

## Painel da Oficina (apps/mrtruck-painel)
Abre as Fichas (../mrtruck/) e o Controle de Estoque (../mrtruck-estoque/) lado a lado no computador, ao vivo. Mesmo login nas duas telas. Divisor arrastável, ampliar, trocar lados, um em cima do outro, tela cheia; dá para instalar como app no Chrome.

## MR Truck Service — pedidos de mudança pelo WhatsApp (modo "Keller aprova")
- Cliente: MR Truck Service (São Manuel-SP), contato Fernando, WhatsApp (14) 99766-5980. Cadastrado no motor com `modo: "keller"`.
- Neste cliente **quem aprova é o Keller**, não o cliente. O motor não fala nada com o Fernando. NUNCA use `mensagemCliente` nos pedidos dele (o motor recusa); use `mensagemKeller`.
- Pastas:
  - Fichas: teste `apps/mrtruck-teste/` → oficial `apps/mrtruck/`
  - Estoque: teste `apps/mrtruck-estoque-teste/` → oficial `apps/mrtruck-estoque/`
  - Painel (só moldura, abre os dois oficiais lado a lado): `apps/mrtruck-painel/`
- Links de teste: https://kellercamilodeoliveira-del.github.io/apps/mrtruck-teste/ e https://kellercamilodeoliveira-del.github.io/apps/mrtruck-estoque-teste/
- Fazer a mudança SÓ nas pastas de teste (as duas falam com o mesmo Firebase do oficial — não mudar coleções nem formato dos dados; a baixa no estoque é lida pelos dois apps).
- Testes automáticos (obrigatório antes de mandar pro Keller): `bash tests/mrtruck/rodar.sh` na raiz do repositório. Tem que terminar com "TUDO OK". Se a mudança quebrar um teste porque mudou de propósito um texto/botão que o teste procura, ajuste o teste junto.
- Publicar (só com o pedido "aprovado"): `bash scripts/publica-mrtruck.sh fichas|estoque|tudo`, conferir `git diff --stat`, rodar os testes com `FICHAS=mrtruck ESTOQUE=mrtruck-estoque bash tests/mrtruck/rodar.sh`, commit e push. Os aparelhos se atualizam sozinhos.
- Regras de negócio já decididas: número da OS digitado à mão, nunca repete nem pula; Orçamento = OS sem número; Lembretes por caminhão (placa/chassi); Estoque só tem cadastro de peça, mínimo/máximo, entrada ("chegou peça") e alerta — a saída é só pela OS finalizada (nada de baixa manual). Público: pessoas com pouca prática de celular/computador — botões grandes e texto simples.

## Prospecção Keller IA (uso interno do Keller — não é app de cliente)
- App: https://kellercamilodeoliveira-del.github.io/apps/prospeccao/ (PWA, instala no computador pelo botão "Instalar no computador").
- Lista de empresas encontradas: `apps/prospeccao/leads.json` (um objeto por empresa: id, n, f = oficina|logistica|estoque, c, e, t, w, p, o, x, s, ad). A busca automática diária ("Prospecção da região – oficinas, transporte e estoque") acrescenta empresas novas nesse arquivo e faz push; nunca apaga nem repete (confere nome e telefone).
- Status (contatada / descartada) e empresas adicionadas à mão ficam no Firebase `escritorio-c3acb`, no documento `os_oficinas/keller-ia-prospeccao` (subcoleções `status` e `extras`). Usa as mesmas regras das Fichas de Serviço: o administrador é o mesmo do Ponto; cada pessoa liberada é um `os_usuarios/{uid}` com `oficinaId: 'keller-ia-prospeccao'`. Esse documento aparece na lista de oficinas do painel do MR Truck como "Keller IA – Prospecção (não é oficina)": não mexer nele por lá.
- Quem libera acesso: o Keller, na parte "Quem tem acesso" do próprio app.
