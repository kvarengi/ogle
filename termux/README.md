# 📱 OGLE CLI для Android (Termux)

Установите OGLE в виде команды `ogle` за 1 минуту.

## Установка (1 строка)
```
pkg install -y curl && curl -fsSL https://raw.githubusercontent.com/kvarengi/ogle/main/termux/install.sh | bash
```

## Запуск
```
ogle            # консоль OGLE (по умолчанию)
ogle run        # то же самое
ogle node       # запустить OGLE NODE (оффчейн-рынок)
ogle web        # веб-интерфейс (требует Flask)
ogle update     # обновить OGLE из репозитория
ogle uninstall  # удалить команду ogle (проект остаётся в $HOME/ogle)
```

## Команды внутри OGLE (консоль)
- `catalog` — каталог космических тел
- `buy <номер>` — купить тело
- `status`, `gravity` — статусы и статистика
- `calibrate`, `gyro start` — калибровка и запуск сборщика нутации

Если GitHub недоступен — скопируйте проект вручную в `$HOME/ogle` и запустите `install.sh` локально: `bash termux/install.sh`.
