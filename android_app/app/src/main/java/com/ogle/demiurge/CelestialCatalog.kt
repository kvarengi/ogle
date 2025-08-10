package com.ogle.demiurge

/**
 * Каталог космических тел для Android-приложения
 * Версия с сокращённым списком для мобильного интерфейса
 */
data class CelestialBody(
    val id: String,
    val name: String,
    val type: String,
    val price: Float,
    val discoveryChance: Float,
    val description: String,
    var owner: String? = null
)

class CelestialCatalog {
    
    private val bodies = mutableListOf<CelestialBody>()
    
    init {
        initializeCatalog()
    }
    
    private fun initializeCatalog() {
        bodies.addAll(listOf(
            CelestialBody(
                id = "BH_001",
                name = "Бездонная Печаль Русской Души",
                type = "Чёрная дыра (бездонная русская печаль)",
                price = 500000f,
                discoveryChance = 0.015f,
                description = "Сия чёрная дыра глубока, как печаль в русской душе на просторах степных. Словно омут в реке - манит и страшит одновременно."
            ),
            
            CelestialBody(
                id = "ST_O_001", 
                name = "Синий Богатырь Небесный",
                type = "Звезда-витязь класса O (синий богатырь)",
                price = 850000f,
                discoveryChance = 0.008f,
                description = "Витязь-звезда в доспехах синих, что сверкает ярче самоцветов уральских. Стоит на страже небесной, как богатырь на заставе."
            ),
            
            CelestialBody(
                id = "PL_T_001",
                name = "Новая Русь Заповедная", 
                type = "Планета-матушка (земная твердь)",
                price = 1200000f,
                discoveryChance = 0.032f,
                description = "Планета-матушка с полями васильковыми и реками медовыми. Где берёзки белоствольные растут под звёздами."
            ),
            
            CelestialBody(
                id = "CM_001",
                name = "Огненная Коса Жар-Птицы",
                type = "Небесная странница с огненной косой", 
                price = 75000f,
                discoveryChance = 0.125f,
                description = "Небесная странница с косой огненной, что развевается по просторам звёздным. Словно жар-птица пролетает над мирами."
            ),
            
            CelestialBody(
                id = "PS_001",
                name = "Маяк Васильковых Полей",
                type = "Звезда-маяк (пульсирующий страж)",
                price = 950000f, 
                discoveryChance = 0.012f,
                description = "Звезда-маяк, что мигает среди васильковых космических полей. Её пульс бьётся в ритме русского сердца."
            ),
            
            CelestialBody(
                id = "WD_001",
                name = "Дедушка Мороз Космический",
                type = "Звёздочка-старушка (белый карлик)",
                price = 320000f,
                discoveryChance = 0.045f,
                description = "Старенькая звёздочка-дедушка, что уже отдала всё тепло свое детушкам-планетам. Белая борода её сияет в космической стуже."
            ),
            
            CelestialBody(
                id = "AS_001", 
                name = "Каменный Странник Ермак",
                type = "Каменный странник",
                price = 45000f,
                discoveryChance = 0.156f,
                description = "Странник каменный, что бродит по просторам космическим уже тысячи лет. В недрах его спрятаны металлы редкие."
            ),
            
            CelestialBody(
                id = "MN_001",
                name = "Верный Товарищ Иван", 
                type = "Спутник-верный товарищ",
                price = 180000f,
                discoveryChance = 0.067f,
                description = "Спутник верный и надёжный, что охраняет планету-матушку от комет злых и астероидов буйных. Характер у него русский - простой и открытый."
            )
        ))
    }
    
    fun getAllBodies(): List<CelestialBody> {
        return bodies.toList()
    }
    
    fun getAvailableBodies(): List<CelestialBody> {
        return bodies.filter { it.owner == null }
    }
    
    fun getSoldBodies(): List<CelestialBody> {
        return bodies.filter { it.owner != null }
    }
    
    fun getSoldCount(): Int {
        return bodies.count { it.owner != null }
    }
    
    fun sellBody(index: Int, owner: String): Boolean {
        return if (index in 0 until bodies.size && bodies[index].owner == null) {
            bodies[index].owner = owner
            true
        } else {
            false
        }
    }
    
    fun getBodyById(id: String): CelestialBody? {
        return bodies.find { it.id == id }
    }
    
    fun getBodyByIndex(index: Int): CelestialBody? {
        return if (index in 0 until bodies.size) bodies[index] else null
    }
}
