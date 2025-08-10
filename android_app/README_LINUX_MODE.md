# 🐧 Полноценная Linux-среда внутри Android-приложения

Этот режим позволит демиургу запускать скрипты и инструменты как в обычной Linux-системе прямо на Android-устройстве, без рут-прав, используя Termux + proot-distro (Ubuntu/Debian контейнер).

## Установка в 3 строки (для чайника)
```
pkg update && pkg upgrade -y
pkg install -y proot-distro git python
proot-distro install ubuntu && proot-distro login ubuntu
```

## После входа в Ubuntu
- Клонируйте ваш код демиурга (или перенесите вручную):
```
git clone <URL_ВАШЕГО_РЕПО> ogle && cd ogle
```
- Установите зависимости, запустите скрипты:
```
apt update && apt install -y python3 python3-pip
pip3 install -r requirements.txt
python3 cosmic_demiurge.py
```

## Полезные команды proot-distro
- Список дистрибутивов: `proot-distro list`
- Вход в среду: `proot-distro login ubuntu`
- Перезапуск контейнера: `exit` и снова `proot-distro login ubuntu`
- Удаление: `proot-distro remove ubuntu`

## Где взять Termux
- Устанавливайте Termux только из F-Droid: https://f-droid.org/en/packages/com.termux/
- В Google Play версия устаревшая

## Заметки по производительности
- proot замедляет операции ввода-вывода; держите проект на внутреннем хранилище
- Для сетевых запросов убедитесь, что у Termux есть интернет-доступ

## Безопасность
- Контейнер изолирован от системы (без root)
- Доступ к файлам регулируется разрешениями Android

Удачных путешествий по звёздной Линукс-стезе! ✨
