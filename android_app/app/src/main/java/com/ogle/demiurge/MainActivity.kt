package com.ogle.demiurge

import android.os.Bundle
import android.view.KeyEvent
import android.widget.EditText
import android.widget.ScrollView
import android.widget.TextView
import androidx.appcompat.app.AppCompatActivity
import android.graphics.Typeface
import android.text.method.ScrollingMovementMethod
import android.view.inputmethod.EditorInfo

class MainActivity : AppCompatActivity() {
    
    private lateinit var terminalOutput: TextView
    private lateinit var commandInput: EditText
    private lateinit var scrollView: ScrollView
    private lateinit var terminalInterface: TerminalInterface
    
    private val terminalHistory = mutableListOf<String>()
    
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        
        setupTerminalUI()
        initializeTerminal()
    }
    
    private fun setupTerminalUI() {
        // Создаём UI программно для простоты
        val layout = android.widget.LinearLayout(this).apply {
            orientation = android.widget.LinearLayout.VERTICAL
            setPadding(16, 16, 16, 16)
            setBackgroundColor(android.graphics.Color.BLACK)
        }
        
        // Заголовок
        val title = TextView(this).apply {
            text = "🌟 OGLE Demiurge Terminal 🌟"
            textSize = 18f
            setTextColor(android.graphics.Color.CYAN)
            typeface = Typeface.MONOSPACE
            gravity = android.view.Gravity.CENTER
            setPadding(0, 0, 0, 16)
        }
        
        // Скролл для вывода терминала
        scrollView = ScrollView(this).apply {
            layoutParams = android.widget.LinearLayout.LayoutParams(
                android.widget.LinearLayout.LayoutParams.MATCH_PARENT,
                0,
                1f
            )
        }
        
        // Вывод терминала
        terminalOutput = TextView(this).apply {
            textSize = 12f
            setTextColor(android.graphics.Color.GREEN)
            typeface = Typeface.MONOSPACE
            movementMethod = ScrollingMovementMethod()
            setPadding(8, 8, 8, 8)
            text = "Инициализация демиурга...\n"
        }
        
        scrollView.addView(terminalOutput)
        
        // Поле ввода команд
        commandInput = EditText(this).apply {
            hint = "Введите команду..."
            textSize = 14f
            setTextColor(android.graphics.Color.WHITE)
            setHintTextColor(android.graphics.Color.GRAY)
            typeface = Typeface.MONOSPACE
            setBackgroundColor(android.graphics.Color.rgb(32, 32, 32))
            setPadding(8, 8, 8, 8)
            
            // Обработка Enter
            setOnEditorActionListener { _, actionId, _ ->
                if (actionId == EditorInfo.IME_ACTION_DONE) {
                    executeCommand()
                    true
                } else false
            }
            
            // Обработка клавиши Enter
            setOnKeyListener { _, keyCode, event ->
                if (keyCode == KeyEvent.KEYCODE_ENTER && event.action == KeyEvent.ACTION_DOWN) {
                    executeCommand()
                    true
                } else false
            }
        }
        
        layout.addView(title)
        layout.addView(scrollView)
        layout.addView(commandInput)
        
        setContentView(layout)
    }
    
    private fun initializeTerminal() {
        terminalInterface = TerminalInterface(this)
        
        val initMessage = terminalInterface.initialize()
        appendToTerminal(initMessage)
        appendToTerminal("\n> Введите команду:")
    }
    
    private fun executeCommand() {
        val command = commandInput.text.toString().trim()
        if (command.isNotEmpty()) {
            // Добавляем команду в историю
            terminalHistory.add(command)
            
            // Показываем команду в терминале
            appendToTerminal("\n💻 > $command")
            
            // Выполняем команду
            val result = terminalInterface.processCommand(command)
            appendToTerminal("\n$result")
            
            // Проверяем команду выхода
            if (command.lowercase() in listOf("exit", "выход")) {
                finish()
                return
            }
            
            appendToTerminal("\n> Введите команду:")
            
            // Очищаем поле ввода
            commandInput.setText("")
            
            // Прокручиваем вниз
            scrollToBottom()
        }
    }
    
    private fun appendToTerminal(text: String) {
        runOnUiThread {
            terminalOutput.append(text)
            scrollToBottom()
        }
    }
    
    private fun scrollToBottom() {
        scrollView.post {
            scrollView.fullScroll(ScrollView.FOCUS_DOWN)
        }
    }
    
    override fun onResume() {
        super.onResume()
        // Фокус на поле ввода
        commandInput.requestFocus()
    }
    
    override fun onDestroy() {
        super.onDestroy()
        // Останавливаем измерения гироскопа при закрытии
        terminalInterface.processCommand("gyro stop")
    }
}
