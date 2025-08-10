#!/data/data/com.termux/files/usr/bin/bash
set -euo pipefail

# OGLE Termux installer
# One-liner: pkg install -y curl && curl -fsSL https://raw.githubusercontent.com/kvarengi/ogle/main/termux/install.sh | bash

echo "🌟 Устанавливаю OGLE в Termux..."

PKGS=(python git curl)

echo "📦 Обновляю пакеты..."
pkg update -y && pkg upgrade -y

echo "📦 Устанавливаю зависимости: ${PKGS[*]}"
pkg install -y ${PKGS[*]}

# Каталог установки
OGLEDIR="$HOME/ogle"
if [ ! -d "$OGLEDIR/.git" ]; then
  echo "🔽 Клонирую репозиторий..."
  git clone https://github.com/kvarengi/ogle.git "$OGLEDIR"
else
  echo "🔁 Репозиторий уже есть, обновляю..."
  cd "$OGLEDIR" && git pull --rebase
fi

cd "$OGLEDIR"

echo "🐍 Ставлю Python-зависимости..."
pip install --upgrade pip
pip install -r requirements.txt || true

# Бинарь ogle с подкомандами
BIN="$PREFIX/bin/ogle"
echo "⚙️  Создаю команду ogle ($BIN)"
cat > "$BIN" <<'EOF'
#!/data/data/com.termux/files/usr/bin/bash
set -e
APPDIR="$HOME/ogle"
cd "$APPDIR"

cmd="${1:-run}"
case "$cmd" in
  run)
    shift || true
    exec python3 russian_soul_interface.py "$@" ;;
  node)
    shift || true
    pip install fastapi uvicorn pydantic >/dev/null 2>&1 || true
    exec python3 ogle_node.py "$@" ;;
  web)
    shift || true
    pip install -r requirements.txt >/dev/null 2>&1 || true
    exec python3 cosmic_web_interface.py "$@" ;;
  update)
    git -C "$APPDIR" pull --rebase && echo "✅ OGLE обновлён" ;;
  uninstall)
    rm -f "$PREFIX/bin/ogle"
    echo "⚠️ Wrapper удалён. Проект остаётся в $APPDIR"
    ;;
  *)
    cat <<USAGE
OGLE CLI (Termux)

Использование:
  ogle                # запустить консоль OGLE (по умолчанию)
  ogle run            # то же самое
  ogle node           # запустить OGLE NODE (оффчейн-рынок)
  ogle web            # запустить веб-интерфейс
  ogle update         # обновить OGLE из репозитория
  ogle uninstall      # удалить команду ogle
USAGE
    ;;
 esac
EOF
chmod +x "$BIN"

echo "✅ Готово! Запускайте: ogle"
echo "💡 Подкоманды: run | node | web | update | uninstall"
