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
