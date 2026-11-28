#!/bin/bash
# Roda os testes automáticos da MR Truck (Fichas + Estoque) na versão de TESTE, com um Firebase falso.
# Uso (da raiz do repositório):  bash tests/mrtruck/rodar.sh
# Para testar a oficial:          FICHAS=mrtruck ESTOQUE=mrtruck-estoque bash tests/mrtruck/rodar.sh
# Saída: o que cada teste viu na tela + "errs [...]" (erros de JavaScript). Tem que terminar com "TUDO OK".
cd "$(dirname "$0")/../.."
python3 -c "import playwright" 2>/dev/null || pip install -q playwright --break-system-packages
python3 -m playwright install chromium >/dev/null 2>&1 || true
curl -s -o /dev/null http://localhost:8765/ || { nohup python3 -m http.server 8765 >/tmp/mrtruck-servidor.log 2>&1 & sleep 1; }
mkdir -p /tmp/mrtruck-testes
falhou=0
for t in os_numero_orcamento lembretes busca_caminhao sugestoes pagamento estoque_integrado abrindo_travado pdf; do
  echo "===== $t"
  saida=$(timeout 300 python3 "tests/mrtruck/$t.py" 2>&1); cod=$?
  echo "$saida"
  if [ $cod -ne 0 ] || echo "$saida" | grep -E "^errs|errs \[" | grep -vq "\[\]"; then echo "!!!!! $t FALHOU"; falhou=1; fi
done
[ $falhou = 0 ] && echo "TUDO OK (prints em /tmp/mrtruck-testes)" || { echo "ALGUM TESTE FALHOU"; exit 1; }
