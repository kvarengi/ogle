# 📱 OGLE CLI для Android (Termux)

Установите OGLE в виде команды `ogle` в Termux за 1 минуту.

## Установка (3 строки)
```
pkg update && pkg upgrade -y
pkg install -y curl
curl -fsSL https://raw.githubusercontent.com/kvarengi/ogle/main/termux/install.sh | bash
```

## Запуск
```
ogle
```

## Команды внутри OGLE
- `catalog` — каталог космических тел
- `buy <номер>` — купить тело
- `status`, `gravity` — статусы и статистика
- `calibrate`, `gyro start` — калибровка и запуск сборщика нутации

Если нет интернета или GitHub недоступен — скопируйте проект вручную в `$HOME/ogle` и повторно запустите `install.sh`.
