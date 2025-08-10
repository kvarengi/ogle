#!/bin/bash

# Скрипт для сборки и установки Android-приложения OGLE Demiurge

echo "🌟 Сборка Android-приложения OGLE Demiurge..."
echo "=" * 60

# Проверяем наличие Android SDK
if ! command -v adb &> /dev/null; then
    echo "❌ Android SDK не найден. Установите Android Studio."
    exit 1
fi

# Переходим в директорию проекта
cd "$(dirname "$0")"

echo "📱 Проверяем подключенные устройства..."
adb devices

echo ""
echo "🔨 Собираем debug-версию..."
./gradlew clean assembleDebug

if [ $? -eq 0 ]; then
    echo "✅ Сборка завершена успешно!"
    
    # Проверяем, подключено ли устройство
    device_count=$(adb devices | grep -c "device$")
    
    if [ $device_count -gt 0 ]; then
        echo ""
        echo "📲 Устанавливаем на подключенное устройство..."
        adb install -r app/build/outputs/apk/debug/app-debug.apk
        
        if [ $? -eq 0 ]; then
            echo "✅ Установка завершена успешно!"
            echo ""
            echo "🚀 Запускаем приложение..."
            adb shell am start -n com.ogle.demiurge/.MainActivity
            echo ""
            echo "🌟 OGLE Demiurge запущен на устройстве!"
            echo "📱 Демиург готов собирать нутацию с гироскопа!"
        else
            echo "❌ Ошибка при установке"
        fi
    else
        echo "⚠️ Устройство не подключено. APK создан в:"
        echo "   app/build/outputs/apk/debug/app-debug.apk"
        echo ""
        echo "📲 Для установки подключите устройство и выполните:"
        echo "   adb install app/build/outputs/apk/debug/app-debug.apk"
    fi
else
    echo "❌ Ошибка при сборке"
    exit 1
fi

echo ""
echo "🎉 Готово! Демиург-творец гравитации в вашем кармане!"
