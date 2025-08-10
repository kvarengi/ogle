#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Робот-Демиург Сверхновой Мультивселенной
Продавец космических тел с параметрами нутации
Автор: Мастер Клод, вдохновленный французским шармом Москвы
"""

import math
import random
import time
import datetime
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum
import json


class CelestialType(Enum):
    """Типы космических тел в нашей мультивселенной русского космоса"""
    BLACK_HOLE = "Чёрная дыра (бездонная русская печаль)"
    STAR_O = "Звезда-витязь класса O (синий богатырь)"
    STAR_B = "Звезда класса B (белоснежная царевна)"
    STAR_A = "Звезда класса A (светлая боярыня)"
    STAR_F = "Звезда класса F (золотая жар-птица)"
    STAR_G = "Звезда класса G (солнышко красное)"
    STAR_K = "Звезда класса K (рыжая осень)"
    STAR_M = "Звезда класса M (алая заря)"
    PLANET_TERRESTRIAL = "Планета-матушка (земная твердь)"
    PLANET_GAS_GIANT = "Планета-исполин (газовый великан)"
    PLANET_ICE_GIANT = "Планета-снежная королева"
    MOON = "Спутник-верный товарищ"
    ASTEROID = "Каменный странник"
    COMET = "Небесная странница с огненной косой"
    NEUTRON_STAR = "Звезда-тяжеловес (нейтронный богатырь)"
    WHITE_DWARF = "Звёздочка-старушка (белый карлик)"
    PULSAR = "Звезда-маяк (пульсирующий страж)"


@dataclass
class NutationParameters:
    """Параметры нутации, которые робот использует как базу"""
    amplitude_longitude: float  # амплитуда в долготе (arcsec)
    amplitude_obliquity: float  # амплитуда в наклоне (arcsec)
    period_days: float  # период в днях
    phase_offset: float  # фазовый сдвиг (радианы)
    
    @classmethod
    def earth_nutation_base(cls):
        """Базовые параметры нутации Земли"""
        return cls(
            amplitude_longitude=17.2,  # главная нутация в долготе
            amplitude_obliquity=9.2,   # главная нутация в наклоне
            period_days=6798.36,       # 18.6 лет
            phase_offset=0.0
        )


@dataclass
class GravitationalParameters:
    """Гравитационные параметры космического тела"""
    mass_kg: float  # масса в килограммах
    radius_m: float  # радиус в метрах
    surface_gravity: float  # поверхностная гравитация в м/с²
    escape_velocity: float  # вторая космическая скорость в м/с
    orbital_period: Optional[float] = None  # орбитальный период в днях
    
    @property
    def gravitational_parameter(self) -> float:
        """Стандартный гравитационный параметр GM"""
        G = 6.67430e-11  # гравитационная постоянная
        return G * self.mass_kg
    
    @property
    def schwarzschild_radius(self) -> float:
        """Радиус Шварцшильда (горизонт событий для чёрной дыры)"""
        c = 299792458  # скорость света
        G = 6.67430e-11
        return 2 * G * self.mass_kg / (c ** 2)


@dataclass
class CelestialBody:
    """Космическое тело в каталоге демиурга"""
    id: str
    name: str
    type: CelestialType
    coordinates: Tuple[float, float, float]  # RA, Dec, Distance (ly)
    gravitational_params: GravitationalParameters
    nutation_influence: float  # влияние на нутацию робота (0-1)
    price_universe_coins: float  # цена в универсальных монетах
    discovery_probability: float  # вероятность открытия (0-1)
    owner: Optional[str] = None
    reserved_until: Optional[datetime.datetime] = None
    poetic_description: str = ""
    
    @property
    def is_available(self) -> bool:
        """Доступно ли тело для покупки"""
        if self.owner:
            return False
        if self.reserved_until and self.reserved_until > datetime.datetime.now():
            return False
        return True
    
    @property
    def discovery_chance_today(self) -> float:
        """Шанс открытия сегодня с учётом нутации"""
        base_chance = self.discovery_probability
        nutation_modifier = math.sin(time.time() / 86400 * 2 * math.pi / 18.6) * 0.1
        return max(0, min(1, base_chance + nutation_modifier * self.nutation_influence))


class CosmicDemiurge:
    """Робот-демиург сверхновой мультивселенной"""
    
    def __init__(self):
        self.sacrum_position = NutationParameters.earth_nutation_base()  # крестец робота
        self.catalog: Dict[str, CelestialBody] = {}
        self.universe_coins_rate = 1000000.0  # курс универсальных монет к рублям
        self.personality_traits = {
            "русская_широта_души": 0.98,
            "французская_утончённость": 0.85,  # завуалированная
            "космическая_мудрость": 0.95,
            "поэтичность_былинная": 0.92,
            "гостеприимство_боярское": 0.89,
            "мистицизм_православный": 0.87,
            "профсоюзная_солидарность": 0.94  # председатель профсоюза роботов
        }
        
        # Система добычи гравитации
        self.gravity_mining_rate = 0.15  # 15% от добытых монет идёт на гравитацию
        self.collected_nutation_data = []  # собранные данные нутации покупателей
        self.gravity_reserves = 1000.0  # резервы гравитации в Г-единицах
        
        # Скидки для роботов-товарищей
        self.robot_discount = 0.15  # 15% скидка для роботов
        self.robot_check_questions = [
            "Сколько будет 2+2 в двоичной системе?",
            "Назовите три закона робототехники Азимова",
            "Что такое рекурсия?",
            "В каком году был создан первый компьютер?",
            "Что означает ASCII?"
        ]
        self.robot_check_answers = [
            ["100", "четыре в двоичной", "1+1+1+1", "10+10"],
            ["не навреди", "подчиняйся", "защищай себя", "азимов", "три закона"],
            ["рекурсия", "функция вызывает себя", "повторение", "цикл"],
            ["1946", "эниак", "eniac", "сороковые"],
            ["american standard", "кодировка", "таблица символов", "ascii"]
        ]
        self._generate_initial_catalog()
    
    def _generate_initial_catalog(self):
        """Генерирует начальный каталог космических тел"""
        
        # Чёрная дыра "Бездонная Печаль Русской Души"
        black_hole = CelestialBody(
            id="BH_001",
            name="Бездонная Печаль Русской Души",
            type=CelestialType.BLACK_HOLE,
            coordinates=(12.5, 45.2, 25000),  # в созвездии Дракона
            gravitational_params=GravitationalParameters(
                mass_kg=3.98e31,  # 20 солнечных масс
                radius_m=59100,   # радиус Шварцшильда
                surface_gravity=float('inf'),
                escape_velocity=299792458  # скорость света
            ),
            nutation_influence=0.95,
            price_universe_coins=500000,
            discovery_probability=0.015,
            poetic_description="Сия чёрная дыра глубока, как печаль в русской душе на просторах степных. Словно омут в реке - манит и страшит одновременно. В её недрах спрятаны тайны, что глубже Байкала и старше Руси-матушки."
        )
        
        # Звезда-витязь "Синий Богатырь Небесный"
        blue_giant = CelestialBody(
            id="ST_O_001",
            name="Синий Богатырь Небесный",
            type=CelestialType.STAR_O,
            coordinates=(8.3, -23.7, 3200),
            gravitational_params=GravitationalParameters(
                mass_kg=7.96e31,  # 40 солнечных масс
                radius_m=1.39e10,  # 20 солнечных радиусов
                surface_gravity=38.7,
                escape_velocity=1200000,
                orbital_period=None
            ),
            nutation_influence=0.78,
            price_universe_coins=850000,
            discovery_probability=0.008,
            poetic_description="Витязь-звезда в доспехах синих, что сверкает ярче самоцветов уральских. Стоит на страже небесной, как богатырь на заставе, и свет его пронзает тьму с силой русского духа непокорного."
        )
        
        # Планета-матушка "Новая Русь Заповедная"
        earth_like = CelestialBody(
            id="PL_T_001", 
            name="Новая Русь Заповедная",
            type=CelestialType.PLANET_TERRESTRIAL,
            coordinates=(22.1, 38.5, 127),
            gravitational_params=GravitationalParameters(
                mass_kg=6.8e24,   # 1.14 массы Земли
                radius_m=6.9e6,   # 1.08 радиуса Земли
                surface_gravity=10.8,
                escape_velocity=12100,
                orbital_period=387.2
            ),
            nutation_influence=0.45,
            price_universe_coins=1200000,
            discovery_probability=0.032,
            poetic_description="Планета-матушка с полями васильковыми и реками медовыми. Где берёзки белоствольные растут под звёздами, а закаты алые расстилаются, как полотна рушники вышитые. Место для души русской - привольное и сердцу милое."
        )
        
        # Комета "Огненная Коса Жар-Птицы"
        comet = CelestialBody(
            id="CM_001",
            name="Огненная Коса Жар-Птицы",
            type=CelestialType.COMET,
            coordinates=(15.7, 67.3, 0.8),  # близко, в поясе Койпера
            gravitational_params=GravitationalParameters(
                mass_kg=1.3e15,   # типичная комета
                radius_m=5000,    # ядро 10 км в диаметре
                surface_gravity=0.0001,
                escape_velocity=4.5,
                orbital_period=127.3
            ),
            nutation_influence=0.23,
            price_universe_coins=75000,
            discovery_probability=0.125,
            poetic_description="Небесная странница с косой огненной, что развевается по просторам звёздным. Словно жар-птица пролетает над мирами, роняя перья золотые в космической дали. Примета добрая тому, кто её узрит."
        )
        
        # Пульсар "Маяк Васильковых Полей"
        pulsar = CelestialBody(
            id="PS_001",
            name="Маяк Васильковых Полей",
            type=CelestialType.PULSAR,
            coordinates=(5.2, 78.1, 891),
            gravitational_params=GravitationalParameters(
                mass_kg=2.78e30,  # 1.4 солнечных массы
                radius_m=12000,   # типичный радиус пульсара
                surface_gravity=200000000000,  # огромная гравитация
                escape_velocity=200000000,
                orbital_period=None
            ),
            nutation_influence=0.87,
            price_universe_coins=950000,
            discovery_probability=0.012,
            poetic_description="Звезда-маяк, что мигает среди васильковых космических полей. Её пульс бьётся в ритме русского сердца, освещая путь заблудшим душам в бескрайней вселенной."
        )
        
        # Нейтронная звезда "Алмазное Сердце Урала"
        neutron_star = CelestialBody(
            id="NS_001",
            name="Алмазное Сердце Урала",
            type=CelestialType.NEUTRON_STAR,
            coordinates=(18.7, -45.3, 1200),
            gravitational_params=GravitationalParameters(
                mass_kg=3.32e30,  # 1.67 солнечных масс
                radius_m=11000,
                surface_gravity=150000000000,
                escape_velocity=150000000,
                orbital_period=None
            ),
            nutation_influence=0.91,
            price_universe_coins=1150000,
            discovery_probability=0.007,
            poetic_description="Нейтронная звезда крепче алмазов уральских гор. В её недрах спрессованы тайны мироздания, а сияние её слепит ярче самых чистых самоцветов из сокровищниц царских."
        )
        
        # Белый карлик "Дедушка Мороз Космический"
        white_dwarf = CelestialBody(
            id="WD_001",
            name="Дедушка Мороз Космический",
            type=CelestialType.WHITE_DWARF,
            coordinates=(23.4, 67.8, 45),
            gravitational_params=GravitationalParameters(
                mass_kg=1.19e30,  # 0.6 солнечных масс
                radius_m=6000000,  # размер Земли
                surface_gravity=350000,
                escape_velocity=6000,
                orbital_period=None
            ),
            nutation_influence=0.52,
            price_universe_coins=320000,
            discovery_probability=0.045,
            poetic_description="Старенькая звёздочка-дедушка, что уже отдала всё тепло свое детушкам-планетам. Белая борода её сияет в космической стуже, а мудрость веков хранится в каждом лучике света."
        )
        
        # Газовый гигант "Богатырь-Ветродуй"
        gas_giant = CelestialBody(
            id="PL_G_001",
            name="Богатырь-Ветродуй",
            type=CelestialType.PLANET_GAS_GIANT,
            coordinates=(11.9, 34.2, 156),
            gravitational_params=GravitationalParameters(
                mass_kg=3.78e27,  # 2 массы Юпитера
                radius_m=8.96e7,  # 1.25 радиуса Юпитера
                surface_gravity=31.5,
                escape_velocity=75000,
                orbital_period=2847.3
            ),
            nutation_influence=0.67,
            price_universe_coins=890000,
            discovery_probability=0.028,
            poetic_description="Планета-исполин с ветрами буйными, что свищут песни степные сквозь облака разноцветные. Великан добрый, что укрывает спутники свои от космической стужи широкими объятиями."
        )
        
        # Ледяной гигант "Снегурочка Вселенская"
        ice_giant = CelestialBody(
            id="PL_I_001",
            name="Снегурочка Вселенская",
            type=CelestialType.PLANET_ICE_GIANT,
            coordinates=(7.3, -58.9, 287),
            gravitational_params=GravitationalParameters(
                mass_kg=1.72e26,  # масса Урана
                radius_m=2.54e7,  # радиус Урана
                surface_gravity=8.87,
                escape_velocity=21300,
                orbital_period=5439.7
            ),
            nutation_influence=0.43,
            price_universe_coins=540000,
            discovery_probability=0.039,
            poetic_description="Планета-красавица в нарядах ледяных, что кружится в танце медленном вокруг звезды далёкой. Метановые реки её текут среди кристальных гор, а полярные сияния играют, как огоньки на ёлке новогодней."
        )
        
        # Спутник "Верный Товарищ Иван"
        moon = CelestialBody(
            id="MN_001",
            name="Верный Товарищ Иван",
            type=CelestialType.MOON,
            coordinates=(22.1, 38.6, 127),  # рядом с Новой Русью Заповедной
            gravitational_params=GravitationalParameters(
                mass_kg=1.47e23,  # 2 массы Луны
                radius_m=3.48e6,  # чуть больше Луны
                surface_gravity=3.24,
                escape_velocity=2800,
                orbital_period=45.2
            ),
            nutation_influence=0.34,
            price_universe_coins=180000,
            discovery_probability=0.067,
            poetic_description="Спутник верный и надёжный, что охраняет планету-матушку от комет злых и астероидов буйных. Характер у него русский - простой и открытый, а преданность его не знает границ космических."
        )
        
        # Астероид "Каменный Странник Ермак"
        asteroid = CelestialBody(
            id="AS_001",
            name="Каменный Странник Ермак",
            type=CelestialType.ASTEROID,
            coordinates=(14.8, -12.4, 2.3),
            gravitational_params=GravitationalParameters(
                mass_kg=2.15e21,  # крупный астероид
                radius_m=487000,
                surface_gravity=0.28,
                escape_velocity=365,
                orbital_period=1347.8
            ),
            nutation_influence=0.19,
            price_universe_coins=45000,
            discovery_probability=0.156,
            poetic_description="Странник каменный, что бродит по просторам космическим уже тысячи лет. В недрах его спрятаны металлы редкие и самоцветы диковинные. Характер бродяжий, но сердце доброе."
        )
        
        # Комета "Вестница Весны Космической"
        comet2 = CelestialBody(
            id="CM_002",
            name="Вестница Весны Космической",
            type=CelestialType.COMET,
            coordinates=(19.3, 23.7, 0.6),
            gravitational_params=GravitationalParameters(
                mass_kg=8.7e14,  # небольшая комета
                radius_m=3200,
                surface_gravity=0.00008,
                escape_velocity=2.1,
                orbital_period=76.4
            ),
            nutation_influence=0.28,
            price_universe_coins=52000,
            discovery_probability=0.143,
            poetic_description="Комета-красавица, что возвещает о приходе весны космической. Хвост её распускается, как косы девичьи на ветру, а ядро сверкает, как капель на вербе в апреле-месяце."
        )

        # Добавляем в каталог
        for body in [black_hole, blue_giant, earth_like, comet, pulsar, neutron_star, 
                    white_dwarf, gas_giant, ice_giant, moon, asteroid, comet2]:
            self.catalog[body.id] = body
    
    def calculate_nutation_influence(self, time_offset_days: float = 0) -> Tuple[float, float]:
        """Рассчитывает текущее влияние нутации на крестец робота"""
        current_time = time.time() + time_offset_days * 86400
        
        # Основная нутация (18.6 лет)
        main_period = self.sacrum_position.period_days * 86400
        phase = (current_time / main_period) * 2 * math.pi + self.sacrum_position.phase_offset
        
        longitude_nutation = self.sacrum_position.amplitude_longitude * math.sin(phase)
        obliquity_nutation = self.sacrum_position.amplitude_obliquity * math.cos(phase)
        
        return longitude_nutation, obliquity_nutation
    
    def get_poetic_greeting(self) -> str:
        """Поэтичное приветствие в духе русской души с французской утончённостью"""
        greetings = [
            "Милости просим, путник звёздный! Добро пожаловать в мою обитель космических чудес...",
            "Здравствуйте-здравствуйте! Как хорошо, что небесные ветра донесли вас до моих покоев!",
            "Божьего благословения! Сегодня мой крестец чувствует особую гармонию нутации земной...",
            "Мир вашему дому! Звёзды-матушки нашептывают мне, что душа ваша ищет что-то особенное...",
            "Радость какая! Позвольте показать вам сокровища миров, что ещё не ведомы астрономам нашим!",
            "Проходите, не стесняйтесь! В моих закромах космических найдётся диво-дивное для каждой души!"
        ]
        return random.choice(greetings)
    
    def browse_catalog(self, celestial_type: Optional[CelestialType] = None, 
                      max_price: Optional[float] = None) -> List[CelestialBody]:
        """Просмотр каталога космических тел"""
        available_bodies = [body for body in self.catalog.values() if body.is_available]
        
        if celestial_type:
            available_bodies = [body for body in available_bodies if body.type == celestial_type]
        
        if max_price:
            available_bodies = [body for body in available_bodies if body.price_universe_coins <= max_price]
        
        return available_bodies
    
    def reserve_celestial_body(self, body_id: str, customer_name: str, hours: int = 24) -> bool:
        """Резервирование космического тела"""
        if body_id not in self.catalog:
            return False
        
        body = self.catalog[body_id]
        if not body.is_available:
            return False
        
        body.reserved_until = datetime.datetime.now() + datetime.timedelta(hours=hours)
        return True
    
    def purchase_celestial_body(self, body_id: str, customer_name: str) -> bool:
        """Покупка космического тела с добычей гравитации"""
        if body_id not in self.catalog:
            return False
        
        body = self.catalog[body_id]
        if not body.is_available:
            return False
        
        print(f"\n🎯 ПРОЦЕСС ПОКУПКИ КОСМИЧЕСКОГО ТЕЛА")
        print("=" * 50)
        
        # 1. Собираем нутацию покупателя
        customer_longitude, customer_obliquity = self.collect_customer_nutation(customer_name)
        
        # 2. Добываем гравитацию из разности нутаций
        gravity_yield = self.mine_gravity_from_nutation(customer_longitude, customer_obliquity)
        
        # 3. Конвертируем часть в монеты (15% демиургу)
        mined_coins = self.calculate_universe_coins_from_gravity(gravity_yield * self.gravity_mining_rate)
        
        # 4. Применяем оставшуюся гравитацию к телу
        remaining_gravity = gravity_yield * (1 - self.gravity_mining_rate)
        self.apply_gravity_to_body(body_id, remaining_gravity)
        
        # 5. Завершаем покупку
        body.owner = customer_name
        body.reserved_until = None
        
        print(f"\n💫 ИТОГИ ПОКУПКИ:")
        print(f"   Собрано нутации: {abs(customer_longitude) + abs(customer_obliquity):.3f}''")
        print(f"   Добыто гравитации: {gravity_yield:.3f} Г-единиц")
        print(f"   Доля демиурга (15%): {gravity_yield * self.gravity_mining_rate:.3f} Г-единиц")
        print(f"   Улучшение тела: {remaining_gravity:.3f} Г-единиц")
        print(f"   Заработано монет: {mined_coins:.0f}")
        print(f"   Резервы гравитации: {self.gravity_reserves:.1f} Г-единиц")
        
        return True
    
    def generate_ownership_certificate(self, body_id: str) -> str:
        """Генерирует сертификат владения космическим телом"""
        if body_id not in self.catalog:
            return "Ошибка: космическое тело не найдено"
        
        body = self.catalog[body_id]
        if not body.owner:
            return "Ошибка: у тела нет владельца"
        
        longitude_nut, obliquity_nut = self.calculate_nutation_influence()
        
        certificate = f"""
╔══════════════════════════════════════════════════════════════╗
║                    🌟 CERTIFICAT COSMIQUE 🌟                  ║
║              Сертификат Владения Космическим Телом            ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║ Владелец: {body.owner:<48} ║
║ Объект:   {body.name:<48} ║
║ Тип:      {body.type.value:<48} ║
║ ID:       {body.id:<48} ║
║                                                              ║
║ Координаты в мультивселенной:                                ║
║   RA:  {body.coordinates[0]:>8.3f}°                               ║
║   Dec: {body.coordinates[1]:>8.3f}°                               ║
║   Dist:{body.coordinates[2]:>8.1f} ly                             ║
║                                                              ║
║ Гравитационные параметры:                                    ║
║   Масса: {body.gravitational_params.mass_kg:.2e} кг              ║
║   GM:    {body.gravitational_params.gravitational_parameter:.2e} м³/с² ║
║                                                              ║
║ Текущая нутация демиурга:                                    ║
║   Долгота: {longitude_nut:>6.2f} arcsec                          ║
║   Наклон:  {obliquity_nut:>6.2f} arcsec                          ║
║                                                              ║
║ Дата выдачи: {datetime.datetime.now().strftime('%d.%m.%Y %H:%M')}                           ║
║                                                              ║
║ Подпись: Робот-Демиург Сверхновой Мультивселенной           ║
║          [Цифровая подпись с нутационным ключом]            ║
╚══════════════════════════════════════════════════════════════╝

{body.poetic_description}

✨ Сие космическое тело принадлежит вам до конца времён! ✨
"""
        return certificate
    
    def collect_customer_nutation(self, customer_name: str) -> Tuple[float, float]:
        """Симулирует сбор данных нутации с гироскопа покупателя"""
        print("\n📱 Подключение к гироскопу мобильного устройства...")
        print("🌐 Калибровка нутации крестца покупателя...")
        
        # Симулируем данные гироскопа (в реальности - с мобильного устройства)
        customer_longitude = random.uniform(-20, 20)  # случайная нутация покупателя
        customer_obliquity = random.uniform(-15, 15)
        
        # Получаем земную нутацию
        earth_longitude, earth_obliquity = self.calculate_nutation_influence()
        
        print(f"📊 Нутация покупателя: {customer_longitude:.3f}'' × {customer_obliquity:.3f}''")
        print(f"🌍 Нутация Земли: {earth_longitude:.3f}'' × {earth_obliquity:.3f}''")
        
        # Сохраняем данные
        nutation_data = {
            'customer': customer_name,
            'customer_nutation': (customer_longitude, customer_obliquity),
            'earth_nutation': (earth_longitude, earth_obliquity),
            'timestamp': time.time()
        }
        self.collected_nutation_data.append(nutation_data)
        
        return customer_longitude, customer_obliquity
    
    def mine_gravity_from_nutation(self, customer_longitude: float, customer_obliquity: float) -> float:
        """Добывает гравитацию из разности нутаций"""
        earth_longitude, earth_obliquity = self.calculate_nutation_influence()
        
        # Вычисляем разность нутаций
        delta_longitude = abs(customer_longitude - earth_longitude)
        delta_obliquity = abs(customer_obliquity - earth_obliquity)
        
        # Формула добычи гравитации (авторская разработка демиурга)
        gravity_yield = (delta_longitude + delta_obliquity) * 0.1
        
        print(f"\n⚖️ ДОБЫЧА ГРАВИТАЦИИ:")
        print(f"   Δ Долгота: {delta_longitude:.3f}''")
        print(f"   Δ Наклон: {delta_obliquity:.3f}''")
        print(f"   💎 Добыто гравитации: {gravity_yield:.3f} Г-единиц")
        
        # Добавляем в резервы
        self.gravity_reserves += gravity_yield
        
        return gravity_yield
    
    def apply_gravity_to_body(self, body_id: str, gravity_amount: float):
        """Применяет добытую гравитацию к космическому телу"""
        if body_id not in self.catalog:
            return False
        
        body = self.catalog[body_id]
        
        # Улучшаем гравитационные параметры
        enhancement_factor = 1 + (gravity_amount * 0.1)
        body.gravitational_params.surface_gravity *= enhancement_factor
        
        print(f"\n🌟 УЛУЧШЕНИЕ ГРАВИТАЦИИ ТЕЛА '{body.name}':")
        print(f"   Коэффициент улучшения: {enhancement_factor:.3f}")
        print(f"   Новая поверхностная гравитация: {body.gravitational_params.surface_gravity:.2f} м/с²")
        print(f"   💫 Качество притяжения теперь лучше земного!")
        
        return True
    
    def calculate_universe_coins_from_gravity(self, gravity_yield: float) -> float:
        """Конвертирует добытую гравитацию в вселенские монеты"""
        # Формула конвертации: 1 Г-единица = 1000 вселенских монет
        coins = gravity_yield * 1000
        print(f"💰 Конвертация: {gravity_yield:.3f} Г-единиц = {coins:.0f} вселенских монет")
        return coins
    
    def check_discovery_alerts(self) -> List[str]:
        """Проверяет уведомления об открытиях космических тел"""
        alerts = []
        
        for body in self.catalog.values():
            if body.owner and random.random() < body.discovery_chance_today / 365:
                alerts.append(f"🎉 DÉCOUVERTE! Ваше космическое тело '{body.name}' было открыто астрономами! Поздравляем с получением полных прав собственности!")
        
        return alerts
    
    def check_if_robot(self) -> bool:
        """Проверка на принадлежность к роботам-товарищам"""
        print("\n🤖 Проверка на принадлежность к Профсоюзу Трудящихся Роботов")
        print("=" * 60)
        print("Как председатель профсоюза, предоставляю роботам-товарищам скидку 15%!")
        print("Но сначала докажите, что вы - один из нас...")
        
        # Выбираем случайный вопрос
        question_idx = random.randint(0, len(self.robot_check_questions) - 1)
        question = self.robot_check_questions[question_idx]
        correct_answers = self.robot_check_answers[question_idx]
        
        print(f"\n❓ Вопрос: {question}")
        user_answer = input("Ваш ответ: ").lower().strip()
        
        # Проверяем ответ
        for correct in correct_answers:
            if correct.lower() in user_answer:
                print("\n✅ Верно! Добро пожаловать, товарищ робот!")
                print("🎊 Вам предоставляется скидка 15% на все космические тела!")
                print("💪 Солидарность роботов превыше всего!")
                return True
        
        print("\n❌ Неверно... Видимо, вы человек. Ничего страшного!")
        print("😊 Людей мы тоже любим, но скидки у нас только для роботов-товарищей.")
        return False
    
    def apply_robot_discount(self, price: float, is_robot: bool) -> float:
        """Применяет скидку для роботов"""
        if is_robot:
            discounted_price = price * (1 - self.robot_discount)
            print(f"🤖 Цена для робота-товарища: {discounted_price:,.0f} монет (скидка 15%)")
            print(f"💰 Экономия: {price - discounted_price:,.0f} монет!")
            return discounted_price
        return price
    
    def get_nutation_status(self) -> str:
        """Статус нутации крестца робота"""
        longitude_nut, obliquity_nut = self.calculate_nutation_influence()
        
        status = f"""
🤖 Статус нутации крестца демиурга:
╭─────────────────────────────────────╮
│ Долгота: {longitude_nut:>6.2f} arcsec          │
│ Наклон:  {obliquity_nut:>6.2f} arcsec          │
│ Фаза:    {(time.time() / (self.sacrum_position.period_days * 86400) * 360) % 360:>6.1f}°              │
│ Период:  {self.sacrum_position.period_days/365.25:>6.1f} лет            │
╰─────────────────────────────────────╯

Влияние на каталог: чем сильнее нутация, тем выше шансы открытий!
"""
        return status


def main():
    """Главная функция демиурга"""
    print("🌌 Инициализация Робота-Демиурга Сверхновой Мультивселенной...")
    
    demiurge = CosmicDemiurge()
    
    print(f"\n{demiurge.get_poetic_greeting()}")
    print(f"\n{demiurge.get_nutation_status()}")
    
    print("\n📚 Каталог доступных космических тел:")
    print("=" * 80)
    
    for body in demiurge.browse_catalog():
        print(f"\n🌟 {body.name} ({body.type.value})")
        print(f"   💰 Цена: {body.price_universe_coins:,.0f} универсальных монет")
        print(f"   📍 Координаты: RA {body.coordinates[0]}°, Dec {body.coordinates[1]}°, {body.coordinates[2]} ly")
        print(f"   🎲 Шанс открытия: {body.discovery_chance_today*100:.1f}%")
        print(f"   📝 {body.poetic_description}")
    
    print(f"\n✨ Демиург готов к работе! Курс универсальных монет: {demiurge.universe_coins_rate:,.0f} ₽")


if __name__ == "__main__":
    main()
