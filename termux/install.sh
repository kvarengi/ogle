#!/data/data/com.termux/files/usr/bin/bash
set -euo pipefail

# OGLE Termux installer
# Usage: curl -fsSL https://raw.githubusercontent.com/kvarengi/ogle/main/termux/install.sh | bash

echo "🌟 Устанавливаю OGLE в Termux..."

PKGS=(python git)

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

# Бинарь ogle
BIN="$PREFIX/bin/ogle"
echo "⚙️  Создаю команду ogle ($BIN)"
cat > "$BIN" <<'EOF'
#!/data/data/com.termux/files/usr/bin/bash
set -e
cd "$HOME/ogle"
# Запускаем консольный интерфейс OGLE
exec python3 russian_soul_interface.py "$@"
EOF
chmod +x "$BIN"

echo "✅ Готово! Запускайте: ogle"
echo "💡 Команды внутри OGLE: catalog, buy, status, calibrate, gyro start"
