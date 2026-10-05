#!/bin/bash
# setup-capa-diseno.sh — instala la CAPA DE DISEÑO de motion que usa reel-edita-vdl (revisada 2026-10-02):
#   1) skills oficiales de HyperFrames (núcleo + /motion-graphics) en ~/.claude/skills
#   2) skills internas de motion de HeyGen (motion-doctrine, cut-the-curve, seam-craft, oversized-cursor),
#      fijadas al commit revisado del repo heygen-com/hyperframes (Apache-2.0)
#   3) parche Windows del verificador de cortes (seam-gate.mjs)
#   4) telemetría de HyperFrames desactivada (CLI + media-use)
# NO instala packs de terceros (ver references/11-catalogo-y-recetas.md §Packs revisados).
# Idempotente: se puede relanzar para actualizar. Uso: bash scripts/setup-capa-diseno.sh
set -e
HF_COMMIT=cafb86a4abca32bc0b8b4fdd3de7024ca7fb8201   # commit revisado de heygen-com/hyperframes
HF_CLI=hyperframes@0.8.111                           # versión probada
SK="${CLAUDE_CONFIG_DIR:-$HOME/.claude}/skills"
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
mkdir -p "$SK"

echo "▸ 1/4 skills oficiales de HyperFrames"
ARGS=""
for s in hyperframes hyperframes-animation hyperframes-audio hyperframes-cli hyperframes-core \
         hyperframes-creative hyperframes-keyframes hyperframes-registry hyperframes-studio media-use \
         motion-graphics; do ARGS="$ARGS --skill $s"; done
npx -y skills add https://github.com/heygen-com/hyperframes $ARGS --global --agent claude-code --copy --full-depth --yes \
  | grep -E "✓|Done|rror" || true

echo "▸ 2/4 skills internas de motion de HeyGen @ ${HF_COMMIT:0:7}"
TMP=$(mktemp -d)
git clone -q --filter=blob:none --no-checkout https://github.com/heygen-com/hyperframes.git "$TMP/hf"
git -C "$TMP/hf" sparse-checkout set --no-cone .claude/skills LICENSE >/dev/null 2>&1
git -C "$TMP/hf" checkout -q "$HF_COMMIT"
for s in motion-doctrine cut-the-curve seam-craft oversized-cursor; do
  rm -rf "$SK/$s"; cp -r "$TMP/hf/.claude/skills/$s" "$SK/$s"
  printf '\n<!-- Copiado de heygen-com/hyperframes @ %s (Apache-2.0), .claude/skills/%s, por reel-edita-vdl/scripts/setup-capa-diseno.sh -->\n' "${HF_COMMIT:0:7}" "$s" >> "$SK/$s/SKILL.md"
done
cp "$TMP/hf/LICENSE" "$SK/motion-doctrine/LICENSE-hyperframes"
rm -rf "$TMP"

echo "▸ 3/4 parche del verificador de cortes"
python3 "$HERE/parches/seam-gate-windows.py" "$SK/motion-doctrine/scripts/seam-gate.mjs"

echo "▸ 4/4 telemetría desactivada"
npx -y $HF_CLI telemetry disable >/dev/null 2>&1 || true
if command -v powershell.exe >/dev/null 2>&1; then
  powershell.exe -NoProfile -Command "[Environment]::SetEnvironmentVariable('HYPERFRAMES_NO_TELEMETRY','1','User')" >/dev/null
else
  grep -q HYPERFRAMES_NO_TELEMETRY ~/.profile 2>/dev/null || echo 'export HYPERFRAMES_NO_TELEMETRY=1' >> ~/.profile
fi
npx -y $HF_CLI browser ensure >/dev/null 2>&1 || true
echo "✓ capa de diseño lista. Reinicia la sesión de Claude Code para que carguen las skills."
