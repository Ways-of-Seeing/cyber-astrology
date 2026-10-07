#!/usr/bin/env bash
# Gera o "Cyber Astra.app" — um executável Mac que abre uma janela do
# Terminal amigável (fonte grande, fundo claro, título bonito) rodando
# o modo interativo do Cyber Astra.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
APP_DIR="$ROOT/Cyber Astra.app"
VENV_PY="$ROOT/.venv/bin/python3"

# ── 1. Garante ambiente Python instalado ─────────────────────────────────────
if [ ! -x "$VENV_PY" ]; then
    echo "→ Criando ambiente virtual em .venv…"
    python3 -m venv "$ROOT/.venv"
fi

if ! "$VENV_PY" -c "import cyber_astra" 2>/dev/null; then
    echo "→ Instalando dependências…"
    "$VENV_PY" -m pip install -q -e "$ROOT"
fi

# ── 2. Estrutura do bundle ───────────────────────────────────────────────────
echo "→ Gerando Cyber Astra.app…"
mkdir -p "$APP_DIR/Contents/MacOS"

cat > "$APP_DIR/Contents/Info.plist" <<'PLIST'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN"
  "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleName</key>            <string>Cyber Astra</string>
    <key>CFBundleDisplayName</key>     <string>Cyber Astra</string>
    <key>CFBundleIdentifier</key>      <string>com.cyberastra.app</string>
    <key>CFBundleVersion</key>         <string>2.0.0</string>
    <key>CFBundleShortVersionString</key> <string>2.0.0</string>
    <key>CFBundlePackageType</key>     <string>APPL</string>
    <key>CFBundleExecutable</key>      <string>CyberAstra</string>
    <key>LSMinimumSystemVersion</key>  <string>12.0</string>
    <key>NSHighResolutionCapable</key> <true/>
</dict>
</plist>
PLIST

# ── 3. Executável: abre o Terminal "disfarçado" ──────────────────────────────
cat > "$APP_DIR/Contents/MacOS/CyberAstra" <<'LAUNCHER'
#!/usr/bin/env bash
# Abre uma janela nova do Terminal com visual amigável rodando o Cyber Astra.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
CMD="cd \"$ROOT\" && \"$ROOT/.venv/bin/python3\" -m cyber_astra --app-mode"

ESCAPED_CMD="$(printf '%s' "$CMD" | sed 's/\\/\\\\/g; s/"/\\"/g')"

osascript <<OSA
tell application "Terminal"
    activate
    do script "$ESCAPED_CMD"
    delay 0.3
    set w to front window
    set t to selected tab of w
    set custom title of t to "✨ Cyber Astra — Seu Mapa Astral ✨"
    set title displays custom title of t to true
    set font size of w to 18
    set background color of w to {65535, 65021, 62194}
    set normal text color of w to {11565, 11565, 13878}
    set bold text color of w to {3341, 12079, 24672}
    set cursor color of w to {3341, 12079, 24672}
end tell
OSA
LAUNCHER

chmod +x "$APP_DIR/Contents/MacOS/CyberAstra"

# ── 4. Remove quarentena (app gerado localmente) ─────────────────────────────
xattr -dr com.apple.quarantine "$APP_DIR" 2>/dev/null || true

echo ""
echo "✅ Pronto! Para abrir:"
echo "   open \"$APP_DIR\""
echo "   (ou arraste \"Cyber Astra.app\" para o Dock / Applications)"
