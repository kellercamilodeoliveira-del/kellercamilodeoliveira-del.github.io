#!/bin/bash
# Publica a versão de TESTE da MR Truck na OFICIAL e sobe as versões (os aparelhos se atualizam sozinhos).
# Uso:  bash scripts/publica-mrtruck.sh fichas|estoque|tudo
# Só mexe nos arquivos. Quem roda faz o commit e o push depois.
#   fichas : apps/mrtruck-teste          -> apps/mrtruck           (versões vN)
#   estoque: apps/mrtruck-estoque-teste  -> apps/mrtruck-estoque   (versões eN)
set -e
cd "$(dirname "$0")/../apps"
QUAL="${1:-tudo}"

sobe() { # pasta letra -> imprime o número novo
  local d=$1 l=$2 n
  n=$(grep -o "VERSAO=PREFIXO+'$l[0-9]*'" "$d/sw.js" | grep -o "[0-9]*" | tail -1); n=$((n+1))
  sed -i "s/const VERSAO=PREFIXO+'$l[0-9]*';/const VERSAO=PREFIXO+'$l$n';/" "$d/sw.js"
  echo "$n"
}
marca() { # pasta versão
  sed -i "s/const APP_VERSAO='[^']*';/const APP_VERSAO='$2';/" "$1/index.html"
  echo "{\"v\":\"$2\"}" > "$1/version.json"
  echo "$1 -> $2"
}

if [ "$QUAL" = "fichas" ] || [ "$QUAL" = "tudo" ]; then
  nt=$(sobe mrtruck-teste v); no=$(sobe mrtruck v)
  cp mrtruck-teste/index.html mrtruck/index.html
  sed -i 's|<title>TESTE — Fichas de Serviço</title>|<title>MR Truck — Fichas de Serviço</title>|; s/content="Fichas TESTE">/content="MR Truck">/; s|(arquivo apps/mrtruck-teste/firestore.rules)|(arquivo apps/mrtruck-teste/firestore.rules — já publicado)|' mrtruck/index.html
  for f in mrtruck-teste/*; do b=$(basename "$f"); case "$b" in index.html|sw.js|manifest.json|version.json|firestore.rules) ;; *) cp "$f" "mrtruck/$b";; esac; done
  marca mrtruck-teste "v$nt"; marca mrtruck "v$no"
  grep -qE "TESTE —|Fichas TESTE" mrtruck/index.html && { echo "ERRO: sobrou TESTE na oficial das Fichas"; exit 1; } || true
fi

if [ "$QUAL" = "estoque" ] || [ "$QUAL" = "tudo" ]; then
  nt=$(sobe mrtruck-estoque-teste e); no=$(sobe mrtruck-estoque e)
  cp mrtruck-estoque-teste/index.html mrtruck-estoque/index.html
  sed -i 's|<title>TESTE — Controle de Estoque</title>|<title>Controle de Estoque</title>|; s|content="Estoque TESTE">|content="Estoque">|' mrtruck-estoque/index.html
  for f in mrtruck-estoque-teste/*; do b=$(basename "$f"); case "$b" in index.html|sw.js|manifest.json|version.json) ;; *) cp "$f" "mrtruck-estoque/$b";; esac; done
  marca mrtruck-estoque-teste "e$nt"; marca mrtruck-estoque "e$no"
  grep -qE "TESTE —|Estoque TESTE" mrtruck-estoque/index.html && { echo "ERRO: sobrou TESTE na oficial do Estoque"; exit 1; } || true
fi
echo "Pronto. Confira com: git diff --stat"
