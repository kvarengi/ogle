package com.ogle.demiurge

import android.content.Context
import android.hardware.Sensor
import android.hardware.SensorEvent
import android.hardware.SensorEventListener
import android.hardware.SensorManager
import kotlin.math.*

/**
 * Менеджер гироскопа для сбора нутации крестца покупателя
 * Демиург использует эти данные для добычи гравитации!
 */
class GyroscopeManager(private val context: Context) : SensorEventListener {
    
    private var sensorManager: SensorManager? = null
    private var gyroscope: Sensor? = null
    private var accelerometer: Sensor? = null
    
    // Данные нутации
    private var nutationLongitude: Float = 0f
    private var nutationObliquity: Float = 0f
    private var isCalibrated: Boolean = false
    
    // Базовые значения для калибровки
    private var baseRotationX: Float = 0f
    private var baseRotationY: Float = 0f
    private var baseRotationZ: Float = 0f
    
    // Текущие углы поворота
    private var currentRotationX: Float = 0f
    private var currentRotationY: Float = 0f
    private var currentRotationZ: Float = 0f
    
    // Константы для преобразования в arcsec
    private val RAD_TO_ARCSEC = 206264.806f
    
    // Колбэк для уведомления об изменениях нутации
    var onNutationChanged: ((longitude: Float, obliquity: Float) -> Unit)? = null
    
    init {
        initializeSensors()
    }
    
    private fun initializeSensors() {
        sensorManager = context.getSystemService(Context.SENSOR_SERVICE) as SensorManager
        gyroscope = sensorManager?.getDefaultSensor(Sensor.TYPE_GYROSCOPE)
        accelerometer = sensorManager?.getDefaultSensor(Sensor.TYPE_ACCELEROMETER)
    }
    
    fun startMeasuring() {
        gyroscope?.let { sensor ->
            sensorManager?.registerListener(this, sensor, SensorManager.SENSOR_DELAY_UI)
        }
        accelerometer?.let { sensor ->
            sensorManager?.registerListener(this, sensor, SensorManager.SENSOR_DELAY_UI)
        }
    }
    
    fun stopMeasuring() {
        sensorManager?.unregisterListener(this)
    }
    
    fun calibrate() {
        // Устанавливаем текущие значения как базовые
        baseRotationX = currentRotationX
        baseRotationY = currentRotationY  
        baseRotationZ = currentRotationZ
        isCalibrated = true
    }
    
    override fun onSensorChanged(event: SensorEvent?) {
        event?.let {
            when (it.sensor.type) {
                Sensor.TYPE_GYROSCOPE -> {
                    handleGyroscopeData(it.values)
                }
                Sensor.TYPE_ACCELEROMETER -> {
                    handleAccelerometerData(it.values)
                }
            }
        }
    }
    
    private fun handleGyroscopeData(values: FloatArray) {
        // Обновляем текущие углы поворота
        currentRotationX += values[0] * 0.1f // X-ось (крен)
        currentRotationY += values[1] * 0.1f // Y-ось (тангаж) 
        currentRotationZ += values[2] * 0.1f // Z-ось (рыскание)
        
        if (isCalibrated) {
            calculateNutation()
        }
    }
    
    private fun handleAccelerometerData(values: FloatArray) {
        // Используем акселерометр для дополнительной стабилизации
        // и определения ориентации устройства
    }
    
    private fun calculateNutation() {
        // Вычисляем нутацию крестца на основе отклонений от базовых значений
        val deltaX = currentRotationX - baseRotationX
        val deltaY = currentRotationY - baseRotationY
        val deltaZ = currentRotationZ - baseRotationZ
        
        // Преобразуем в координаты нутации (аналог земной нутации)
        // Используем математическую модель, похожую на астрономическую нутацию
        nutationLongitude = (deltaZ * cos(deltaX.toDouble()) + deltaY * sin(deltaX.toDouble())).toFloat() * RAD_TO_ARCSEC
        nutationObliquity = (deltaY * cos(deltaX.toDouble()) - deltaZ * sin(deltaX.toDouble())).toFloat() * RAD_TO_ARCSEC
        
        // Ограничиваем значения разумными пределами (-20 до +20 arcsec)
        nutationLongitude = nutationLongitude.coerceIn(-20f, 20f)
        nutationObliquity = nutationObliquity.coerceIn(-20f, 20f)
        
        // Уведомляем о изменениях
        onNutationChanged?.invoke(nutationLongitude, nutationObliquity)
    }
    
    fun getNutationData(): Pair<Float, Float> {
        return Pair(nutationLongitude, nutationObliquity)
    }
    
    fun isGyroscopeAvailable(): Boolean {
        return gyroscope != null
    }
    
    fun isAccelerometerAvailable(): Boolean {
        return accelerometer != null
    }
    
    fun getDeviceStatus(): String {
        val gyroStatus = if (isGyroscopeAvailable()) "✅ Доступен" else "❌ Недоступен"
        val accelStatus = if (isAccelerometerAvailable()) "✅ Доступен" else "❌ Недоступен" 
        val calibStatus = if (isCalibrated) "✅ Откалиброван" else "⚠️ Требуется калибровка"
        
        return """
            📱 СТАТУС УСТРОЙСТВА:
            Гироскоп: $gyroStatus
            Акселерометр: $accelStatus
            Калибровка: $calibStatus
            
            🌐 ТЕКУЩАЯ НУТАЦИЯ КРЕСТЦА:
            Долгота: ${String.format("%.3f", nutationLongitude)}''
            Наклон: ${String.format("%.3f", nutationObliquity)}''
        """.trimIndent()
    }
    
    override fun onAccuracyChanged(sensor: Sensor?, accuracy: Int) {
        // Обработка изменения точности сенсоров
    }
}
