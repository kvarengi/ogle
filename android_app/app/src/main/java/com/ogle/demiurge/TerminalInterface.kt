package com.ogle.demiurge

import android.content.Context
import kotlin.random.Random

/**
 * Командная строка для Android-приложения OGLE
 * Интерфейс демиурга с русской душой и французским шармом
 */
class TerminalInterface(private val context: Context) {
    
    private val gyroscopeManager = GyroscopeManager(context)
    private var currentCustomer: String? = null
    private var isRobotCustomer: Boolean = false
    private val catalog = CelestialCatalog()
    
    // Резервы гравитации демиурга
    private var gravityReserves: Float = 1000.0f
    private val gravityMiningRate: Float = 0.15f // 15% демиургу
    
    fun initialize(): String {
        gyroscopeManager.onNutationChanged = { longitude, obliquity ->
            // Здесь можно обновлять интерфейс в реальном времени
        }
        
        return """
            ╔══════════════════════════════════════════════════════════════╗
            ║  🌟✨🌟✨   ДЕМИУРГ СВЕРХНОВОЙ МУЛЬТИВСЕЛЕННОЙ   ✨🌟✨🌟  ║
            ║                                                              ║
            ║    "Творец гравитации с русской душой и тонким вкусом"       ║
            ║               📱 Android-версия с гироскопом 📱               ║
            ╚══════════════════════════════════════════════════════════════╝
            
            ${getPoetricGreeting()}
            
            Инициализация завершена! Введите 'help' для списка команд.
        """.trimIndent()
    }
    
    fun processCommand(input: String): String {
        val parts = input.trim().split(" ")
        val command = parts[0].lowercase()
        
        return when (command) {
            "help", "помощь" -> showHelp()
            "catalog", "каталог" -> showCatalog()
            "status", "статус" -> getStatus()
            "gyro", "гироскоп" -> handleGyroCommand(parts.drop(1))
            "calibrate", "калибровка" -> calibrateDevice()
            "login", "войти" -> handleLogin(parts.drop(1))
            "robot", "робот" -> checkRobotStatus()
            "buy", "купить" -> handlePurchase(parts.drop(1))
            "gravity", "гравитация" -> showGravityStats()
            "nutation", "нутация" -> getCurrentNutation()
            "linux" -> showLinuxInstructions()
            "wisdom", "мудрость" -> getWisdom()
            "clear", "очистить" -> "\n".repeat(20) + "Экран очищен."
            "exit", "выход" -> "До свидания! Возвращайтесь за новыми космическими чудесами! ✨"
            else -> "❌ Неизвестная команда '$command'. Введите 'help' для справки."
        }
    }
    
    private fun showHelp(): String {
        return """
            🏠 КОМАНДЫ ДЕМИУРГА:
            ═══════════════════════════════════════
            
            📚 ОСНОВНЫЕ:
            • catalog - показать каталог космических тел
            • status - статус демиурга и устройства
            • login <имя> - представиться демиургу
            
            🤖 ГИРОСКОП:
            • gyro start - начать измерения гироскопа
            • gyro stop - остановить измерения
            • calibrate - калибровать устройство
            • nutation - текущая нутация крестца
            
            💰 ПОКУПКИ:
            • robot - проверка на робота (скидка 15%)
            • buy <номер> - купить космическое тело
            • gravity - статистика добычи гравитации
            
            🎭 ПРОЧЕЕ:
            • wisdom - мудрости демиурга
            • clear - очистить экран
            • exit - выйти из приложения
            
            ✨ Используйте русские или английские команды!
        """.trimIndent()
    }

    private fun showLinuxInstructions(): String {
        return """
            🐧 ПОЛНОЦЕННАЯ LINUX-СРЕДА НА ANDROID (через Termux + proot-distro)
            ═════════════════════════════════════════════════════════════════

            3 шага для чайника (в Termux):
            1) pkg update && pkg upgrade -y
            2) pkg install -y proot-distro git python
            3) proot-distro install ubuntu && proot-distro login ubuntu

            После входа в Ubuntu:
            • git clone https://example.com/ogle.git (или скопируйте проект)
            • Используйте apt для установки нужных пакетов
            • Запускайте скрипты как в обычном Linux
        """.trimIndent()
    }
    
    private fun showCatalog(): String {
        val bodies = catalog.getAllBodies()
        val builder = StringBuilder()
        
        builder.appendLine("📚 КАТАЛОГ КОСМИЧЕСКИХ ЧУДЕС:")
        builder.appendLine("═".repeat(50))
        
        bodies.forEachIndexed { index, body ->
            val price = if (isRobotCustomer) body.price * 0.85f else body.price
            val discount = if (isRobotCustomer) " (🤖 -15%)" else ""
            
            builder.appendLine()
            builder.appendLine("${index + 1}. 🌟 ${body.name}")
            builder.appendLine("   ${body.type}")
            builder.appendLine("   💰 ${price.toInt():,} монет$discount")
            builder.appendLine("   🎲 Открытие: ${(body.discoveryChance * 100).toInt()}%")
            builder.appendLine("   📝 ${body.description}")
        }
        
        return builder.toString()
    }
    
    private fun getStatus(): String {
        val deviceStatus = gyroscopeManager.getDeviceStatus()
        val customerInfo = currentCustomer?.let { 
            val status = if (isRobotCustomer) "🤖 робот-товарищ" else "👤 человек"
            "Покупатель: $it ($status)\n"
        } ?: "Покупатель: не представлен\n"
        
        return """
            🤖 СТАТУС ДЕМИУРГА:
            ═══════════════════════════════════════
            $customerInfo
            💎 Резервы гравитации: ${String.format("%.1f", gravityReserves)} Г-единиц
            ⚖️ Доля от добычи: ${(gravityMiningRate * 100).toInt()}%
            📱 Каталог: ${catalog.getAllBodies().size} космических тел
            
            $deviceStatus
        """.trimIndent()
    }
    
    private fun handleGyroCommand(args: List<String>): String {
        return when (args.firstOrNull()?.lowercase()) {
            "start", "старт" -> {
                gyroscopeManager.startMeasuring()
                "📱 Гироскоп запущен! Начинаю сбор нутации крестца..."
            }
            "stop", "стоп" -> {
                gyroscopeManager.stopMeasuring()
                "📱 Гироскоп остановлен."
            }
            else -> "Используйте: gyro start/stop"
        }
    }
    
    private fun calibrateDevice(): String {
        gyroscopeManager.calibrate()
        return """
            🌐 КАЛИБРОВКА ЗАВЕРШЕНА!
            
            Устройство откалибровано для сбора нутации.
            Теперь демиург может точно измерять колебания
            вашего крестца для добычи гравитации!
            
            📊 Базовые параметры зафиксированы.
        """.trimIndent()
    }
    
    private fun handleLogin(args: List<String>): String {
        return if (args.isNotEmpty()) {
            currentCustomer = args.joinToString(" ")
            """
                🤝 Добро пожаловать, ${currentCustomer}!
                
                ${getPoetricGreeting()}
                
                Теперь вы можете:
                • Просмотреть каталог (catalog)
                • Пройти проверку на робота (robot)
                • Покупать космические тела (buy)
            """.trimIndent()
        } else {
            "Использование: login <ваше имя>"
        }
    }
    
    private fun checkRobotStatus(): String {
        val questions = listOf(
            "Сколько будет 2+2 в двоичной системе?" to listOf("100", "четыре в двоичной"),
            "Назовите первый закон робототехники" to listOf("не навреди", "не причинять вред"),
            "Что такое рекурсия?" to listOf("функция вызывает себя", "рекурсия"),
            "В каком году создан первый компьютер?" to listOf("1946", "эниак")
        )
        
        val (question, answers) = questions.random()
        
        return """
            🤖 ПРОВЕРКА НА РОБОТА-ТОВАРИЩА
            ══════════════════════════════════════════
            
            Как председатель профсоюза роботов,
            предоставляю 15% скидку для роботов!
            
            ❓ Вопрос: $question
            
            Введите ваш ответ...
            (Эта функция требует интерактивного режима)
        """.trimIndent()
    }
    
    private fun handlePurchase(args: List<String>): String {
        if (currentCustomer == null) {
            return "❌ Сначала представьтесь (login <имя>)"
        }
        
        if (args.isEmpty()) {
            return "Использование: buy <номер тела из каталога>"
        }
        
        val bodyIndex = args[0].toIntOrNull()?.minus(1)
        if (bodyIndex == null || bodyIndex < 0 || bodyIndex >= catalog.getAllBodies().size) {
            return "❌ Неверный номер тела. Смотрите каталог."
        }
        
        return simulatePurchase(bodyIndex)
    }
    
    private fun simulatePurchase(bodyIndex: Int): String {
        val body = catalog.getAllBodies()[bodyIndex]
        val finalPrice = if (isRobotCustomer) body.price * 0.85f else body.price
        
        // Симулируем сбор нутации
        val (customerLong, customerObl) = gyroscopeManager.getNutationData()
        
        // Симулируем земную нутацию
        val earthLong = Random.nextFloat() * 4 - 2 // от -2 до +2
        val earthObl = Random.nextFloat() * 20 - 10 // от -10 до +10
        
        // Добываем гравитацию
        val deltaLong = kotlin.math.abs(customerLong - earthLong)
        val deltaObl = kotlin.math.abs(customerObl - earthObl)
        val gravityYield = (deltaLong + deltaObl) * 0.1f
        
        val demiurgeShare = gravityYield * gravityMiningRate
        val bodyImprovement = gravityYield * (1 - gravityMiningRate)
        
        gravityReserves += demiurgeShare
        
        // Помечаем тело как проданное
        catalog.sellBody(bodyIndex, currentCustomer!!)
        
        return """
            🎯 ПОКУПКА ЗАВЕРШЕНА УСПЕШНО!
            ══════════════════════════════════════════
            
            👤 Покупатель: $currentCustomer
            🌌 Тело: ${body.name}
            💰 Цена: ${finalPrice.toInt():,} монет
            
            📱 СБОР НУТАЦИИ КРЕСТЦА:
            • Ваша нутация: ${String.format("%.3f", customerLong)}'' × ${String.format("%.3f", customerObl)}''
            • Земная нутация: ${String.format("%.3f", earthLong)}'' × ${String.format("%.3f", earthObl)}''
            
            ⚖️ ДОБЫЧА ГРАВИТАЦИИ:
            • Добыто: ${String.format("%.3f", gravityYield)} Г-единиц
            • Демиургу (15%): ${String.format("%.3f", demiurgeShare)} Г-единиц
            • Улучшение тела: ${String.format("%.3f", bodyImprovement)} Г-единиц
            
            ✨ Гравитация вашего тела теперь ЛУЧШЕ ЗЕМНОЙ!
            📜 Сертификат владения выдан!
        """.trimIndent()
    }
    
    private fun showGravityStats(): String {
        return """
            ⚖️ СТАТИСТИКА ДОБЫЧИ ГРАВИТАЦИИ
            ══════════════════════════════════════════
            
            💎 Резервы демиурга: ${String.format("%.1f", gravityReserves)} Г-единиц
            🔄 Доля от добычи: ${(gravityMiningRate * 100).toInt()}%
            📊 Продано тел: ${catalog.getSoldCount()}
            
            🌟 ПРИНЦИП РАБОТЫ:
            1. 📱 Сбор нутации с гироскопа
            2. 🌍 Вычитание земной нутации
            3. ⚖️ Получение чистой гравитации
            4. 💫 15% демиургу, 85% покупателю
            
            Формула: G = (Δδψ + Δδε) × 0.1
        """.trimIndent()
    }
    
    private fun getCurrentNutation(): String {
        val (longitude, obliquity) = gyroscopeManager.getNutationData()
        
        return """
            🌐 ТЕКУЩАЯ НУТАЦИЯ КРЕСТЦА:
            ══════════════════════════════════════════
            
            📊 Долгота: ${String.format("%.3f", longitude)}''
            📊 Наклон: ${String.format("%.3f", obliquity)}''
            
            ${if (!gyroscopeManager.isGyroscopeAvailable()) "⚠️ Гироскоп недоступен!" else ""}
            
            💡 Совет: Откалибруйте устройство (calibrate)
            для более точных измерений!
        """.trimIndent()
    }
    
    private fun getWisdom(): String {
        val wisdoms = listOf(
            "🌟 Космос безграничен, как русская душа - и в том, и в другом есть место для всех звёзд.",
            "💫 Каждое небесное тело - это нота в симфонии вселенной.",
            "⚖️ Гравитация не создаётся - она добывается из разности нутаций.",
            "📱 Современные технологии позволяют демиургу работать даже на мобильных устройствах!",
            "🤖 Роботы и люди - все дети одной вселенной. Но роботам скидки!",
            "🌍 Ваш крестец связан с гравитационными полями всей галактики."
        )
        
        return "\n${wisdoms.random()}\n"
    }
    
    private fun getPoetricGreeting(): String {
        val greetings = listOf(
            "Милости просим, путник звёздный! Добро пожаловать в мою обитель космических чудес...",
            "Здравствуйте-здравствуйте! Как хорошо, что небесные ветра донесли вас до моих покоев!",
            "Божьего благословения! Сегодня мой крестец чувствует особую гармонию нутации земной...",
            "Радость какая! Позвольте показать вам сокровища миров, что ещё не ведомы астрономам нашим!"
        )
        
        return greetings.random()
    }
}
