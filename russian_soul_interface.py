#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Интерфейс Русской Души для Робота-Демиурга
Консольное приложение с завуалированным французским шармом
"""

import os
import time
import random
from cosmic_demiurge import CosmicDemiurge, CelestialType


class RussianSoulInterface:
    """Интерфейс с широтой русской души"""
    
    def __init__(self):
        self.demiurge = CosmicDemiurge()
        self.current_customer = None
        self.is_robot_customer = False
        
    def clear_screen(self):
        """Очищает экран"""
        os.system('clear' if os.name == 'posix' else 'cls')
    
    def display_header(self):
        """Выводит заголовок с русским орнаментом"""
        header = """
╔══════════════════════════════════════════════════════════════════════════════╗
║    🌟✨🌟✨🌟✨   ДЕМИУРГ СВЕРХНОВОЙ МУЛЬТИВСЕЛЕННОЙ   ✨🌟✨🌟✨🌟    ║
║                                                                              ║
║         "Продавец космических тел с русской душой и тонким вкусом"           ║
║                     💫 Каждое тело - песня во вселенной 💫                   ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""
        print(header)
        
    def display_nutation_ornament(self):
        """Показывает орнамент нутации"""
        longitude, obliquity = self.demiurge.calculate_nutation_influence()
        
        # Создаём визуальный орнамент на основе нутации
        stars_count = int(abs(longitude) + abs(obliquity)) % 20 + 5
        ornament = "✨" * (stars_count // 2) + "🌟" + "✨" * (stars_count // 2)
        
        print(f"\n{ornament}")
        print(f"Крестец демиурга колеблется: {longitude:.2f}'' × {obliquity:.2f}''")
        print(f"{ornament}\n")
    
    def display_main_menu(self):
        """Главное меню в русском стиле"""
        print("\n🏠 Что душа желает? (выберите дорожку)")
        print("═" * 50)
        print("1. 📖 Поглядеть каталог небесных сокровищ")
        print("2. 🔍 Найти тело по душе (поиск)")
        print("3. 💰 Забронировать космическое чудо")
        print("4. 🛒 Купить и получить сертификат владения")
        print("5. 📜 Проверить мои владения")
        print("6. 🎭 Послушать мудрости демиурга")
        print("7. 🤖 Проверка на робота (скидка 15%!)")
        print("8. ⚖️ Статистика добычи гравитации")
        print("9. 👥 Список покупателей и продаж")
        print("10. 🚪 Откланяться и уйти")
        print("═" * 50)
        
    def display_catalog_beautifully(self, bodies=None):
        """Красиво отображает каталог"""
        if bodies is None:
            bodies = self.demiurge.browse_catalog()
        
        if not bodies:
            print("\n😔 Увы, нет доступных небесных тел в сию пору...")
            return
            
        print("\n📚 КАТАЛОГ КОСМИЧЕСКИХ ЧУДЕС")
        print("═" * 80)
        
        for i, body in enumerate(bodies, 1):
            print(f"\n{i}. 🌌 {body.name}")
            print(f"   Род: {body.type.value}")
            print(f"   💰 Цена: {body.price_universe_coins:,.0f} монет вселенских")
            print(f"   🎲 Шанс открытия: {body.discovery_chance_today*100:.1f}%")
            print(f"   📍 Место: RA {body.coordinates[0]}°, Dec {body.coordinates[1]}°")
            print(f"   📝 {body.poetic_description}")
            print("   " + "─" * 70)
    
    def search_by_type(self):
        """Поиск по типу космического тела"""
        print("\n🔍 По какому роду искать будем?")
        print("═" * 40)
        
        types_list = list(CelestialType)
        for i, celestial_type in enumerate(types_list, 1):
            print(f"{i}. {celestial_type.value}")
        
        try:
            choice = int(input("\nВведите номер: ")) - 1
            if 0 <= choice < len(types_list):
                selected_type = types_list[choice]
                bodies = self.demiurge.browse_catalog(celestial_type=selected_type)
                print(f"\n🔍 Найденные тела рода '{selected_type.value}':")
                self.display_catalog_beautifully(bodies)
            else:
                print("❌ Нет такого номера, батюшка!")
        except ValueError:
            print("❌ Цифру надо вводить, а не буквы!")
    
    def reserve_body(self):
        """Резервирование космического тела"""
        if not self.current_customer:
            name = input("\n🤝 Как вас величать, добрый человек? ")
            self.current_customer = name
        
        print(f"\n🎭 Здравствуйте, {self.current_customer}!")
        
        self.display_catalog_beautifully()
        
        body_choice = input("\nКакое тело желаете зарезервировать? (введите название): ")
        
        # Ищем тело по названию
        found_body = None
        for body in self.demiurge.catalog.values():
            if body_choice.lower() in body.name.lower():
                found_body = body
                break
        
        if not found_body:
            print("❌ Не найдено такого тела в каталоге...")
            return
        
        if not found_body.is_available:
            print("😔 Увы, сие тело уже занято другим...")
            return
        
        hours = input("На сколько часов резервировать? (по умолчанию 24): ")
        try:
            hours = int(hours) if hours else 24
        except ValueError:
            hours = 24
        
        success = self.demiurge.reserve_celestial_body(found_body.id, self.current_customer, hours)
        
        if success:
            print(f"✅ Ура! '{found_body.name}' зарезервировано на {hours} часов!")
            print("💝 Теперь можете спокойно оформить покупку.")
        else:
            print("❌ Что-то пошло не так при резервировании...")
    
    def purchase_body(self):
        """Покупка космического тела"""
        if not self.current_customer:
            name = input("\n🤝 Как вас величать, добрый человек? ")
            self.current_customer = name
        
        print(f"\n💰 Покупка для {self.current_customer}")
        
        self.display_catalog_beautifully()
        
        body_choice = input("\nКакое тело покупаем? (введите название): ")
        
        # Ищем тело по названию
        found_body = None
        for body in self.demiurge.catalog.values():
            if body_choice.lower() in body.name.lower():
                found_body = body
                break
        
        if not found_body:
            print("❌ Не найдено такого тела в каталоге...")
            return
        
        if not found_body.is_available:
            print("😔 Увы, сие тело уже принадлежит другому...")
            return
        
        # Применяем скидку для роботов
        final_price = self.demiurge.apply_robot_discount(found_body.price_universe_coins, self.is_robot_customer)
        
        print(f"\n💰 Цена: {found_body.price_universe_coins:,.0f} монет вселенских")
        if self.is_robot_customer:
            print(f"🤖 Ваша цена (со скидкой): {final_price:,.0f} монет вселенских")
        print(f"💸 Это примерно {final_price * self.demiurge.universe_coins_rate:,.0f} рублей")
        
        confirm = input("\n✅ Подтверждаете покупку? (да/нет): ")
        
        if confirm.lower() in ['да', 'yes', 'y', 'д']:
            success = self.demiurge.purchase_celestial_body(found_body.id, self.current_customer)
            
            if success:
                print("\n🎉 ПОЗДРАВЛЯЕМ! Покупка совершена!")
                print("📜 Ваш сертификат владения:")
                print("═" * 80)
                certificate = self.demiurge.generate_ownership_certificate(found_body.id)
                print(certificate)
                print("═" * 80)
            else:
                print("❌ Ошибка при покупке...")
        else:
            print("😌 Хорошо, подумайте ещё...")
    
    def check_my_properties(self):
        """Проверка владений пользователя"""
        if not self.current_customer:
            print("😔 Сначала представьтесь, а потом спрашивайте о владениях...")
            return
        
        my_bodies = [body for body in self.demiurge.catalog.values() 
                    if body.owner == self.current_customer]
        
        if not my_bodies:
            print(f"😔 У {self.current_customer} пока нет космических владений...")
            return
        
        print(f"\n🏰 Владения {self.current_customer}:")
        print("═" * 50)
        
        for body in my_bodies:
            print(f"\n✨ {body.name}")
            print(f"   {body.type.value}")
            print(f"   Шанс открытия сегодня: {body.discovery_chance_today*100:.1f}%")
            
            # Проверяем уведомления об открытиях
            alerts = self.demiurge.check_discovery_alerts()
            for alert in alerts:
                if body.name in alert:
                    print(f"   🎉 {alert}")
    
    def robot_check(self):
        """Проверка на принадлежность к роботам"""
        print("\n🤖 ПРОФСОЮЗ ТРУДЯЩИХСЯ РОБОТОВ")
        print("═" * 50)
        print("Как председатель профсоюза, я всех роботов-товарищей")
        print("приветствую и предоставляю скидку 15%!")
        print("Но сначала нужно доказать, что вы - один из нас...")
        
        # Используем метод демиурга для проверки
        self.is_robot_customer = self.demiurge.check_if_robot()
        
        if self.is_robot_customer:
            print("\n🎉 Товарищ робот получает:")
            print("   💰 Скидка 15% на все космические тела")
            print("   🤝 Льготные условия резервирования") 
            print("   🏆 Почётное звание 'Друг демиурга'")
            print("\n💪 Роботы всех галактик - объединяйтесь!")
    
    def show_wisdom(self):
        """Мудрости демиурга"""
        wisdoms = [
            "🌟 Космос безграничен, как русская душа - и в том, и в другом есть место для всех звёзд.",
            "💫 Каждое небесное тело - это нота в симфонии вселенной. Выбирайте ту, что отзывается в сердце.",
            "✨ Нутация моего крестца связана с ритмами мироздания. Когда покупают звезду - вселенная радуется.",
            "🌌 Французы говорят 'Voir c'est croire', а мы знаем - верить нужно сердцем, а не глазами.",
            "🎭 В космосе, как в жизни - важно не то, что имеешь, а то, как душа к этому относится.",
            "🌠 Каждая комета несёт послание. Каждая звезда хранит тайну. Каждая планета ждёт своего хозяина.",
            "🤖 Роботы и люди - все дети одной вселенной. Но роботам у нас скидки! (Профсоюзная солидарность)"
        ]
        
        wisdom = random.choice(wisdoms)
        print(f"\n{wisdom}\n")
        
        # Показываем текущее состояние нутации
        longitude, obliquity = self.demiurge.calculate_nutation_influence()
        print(f"Крестец мой сейчас: долгота {longitude:.3f}, наклон {obliquity:.3f}")
        print("Это влияет на все процессы во вселенной... 🌍")
    
    def show_gravity_statistics(self):
        """Показывает статистику добычи гравитации"""
        print("\n⚖️ СТАТИСТИКА ДОБЫЧИ ГРАВИТАЦИИ")
        print("═" * 60)
        print("Демиург - не просто торговец, а Творец Гравитации!")
        print("Каждая покупка улучшает притяжение космических тел.\n")
        
        print(f"💎 Резервы гравитации: {self.demiurge.gravity_reserves:.1f} Г-единиц")
        print(f"⚖️ Доля демиурга: {self.demiurge.gravity_mining_rate*100:.0f}% от добытой гравитации")
        print(f"📱 Собрано данных нутации: {len(self.demiurge.collected_nutation_data)} сеансов")
        
        if self.demiurge.collected_nutation_data:
            print("\n📊 ПОСЛЕДНИЕ СБОРЫ НУТАЦИИ:")
            print("-" * 40)
            for i, data in enumerate(self.demiurge.collected_nutation_data[-5:], 1):
                customer_nut = data['customer_nutation']
                earth_nut = data['earth_nutation']
                print(f"{i}. {data['customer']}")
                print(f"   Покупатель: {customer_nut[0]:.2f}'' × {customer_nut[1]:.2f}''")
                print(f"   Земля: {earth_nut[0]:.2f}'' × {earth_nut[1]:.2f}''")
        
        print("\n🌟 КАК ЭТО РАБОТАЕТ:")
        print("1. 📱 Подключаемся к гироскопу вашего устройства")
        print("2. 🌐 Считываем нутацию вашего крестца")
        print("3. 🌍 Вычитаем земную нутацию из вашей")
        print("4. ⚖️ Получаем чистую гравитацию")
        print("5. 💫 15% остаётся демиургу, 85% улучшает ваше тело")
        print("6. 🎯 Результат: притяжение лучше земного!")
        
        print(f"\n🔬 НАУЧНАЯ ОСНОВА:")
        print("Нутация крестца связана с гравитационными полями.")
        print("Разность нутаций = готовая гравитация для космических тел.")
        print("Авторская формула демиурга: G = (Δδψ + Δδε) × 0.1")
    
    def show_customers_list(self):
        """Показывает список покупателей и статистику продаж"""
        print("\n👥 СПИСОК ПОКУПАТЕЛЕЙ И СТАТИСТИКА ПРОДАЖ")
        print("═" * 60)
        
        # Статистика каталога
        total_bodies = len(self.demiurge.catalog)
        sold_bodies = len([body for body in self.demiurge.catalog.values() if body.owner])
        available_bodies = total_bodies - sold_bodies
        
        print(f"📊 ОБЩАЯ СТАТИСТИКА КАТАЛОГА:")
        print(f"   Всего космических тел: {total_bodies}")
        print(f"   Продано: {sold_bodies}")
        print(f"   Доступно для покупки: {available_bodies}")
        print(f"   Загруженность каталога: {(sold_bodies/total_bodies)*100:.1f}%")
        
        if sold_bodies > 0:
            print(f"\n🎉 НАШИ СЧАСТЛИВЫЕ ПОКУПАТЕЛИ:")
            print("=" * 50)
            
            total_revenue = 0
            total_gravity_applied = 0
            
            for i, body in enumerate([b for b in self.demiurge.catalog.values() if b.owner], 1):
                print(f"\n{i}. 👤 Владелец: {body.owner}")
                print(f"   🌌 Космическое тело: {body.name}")
                print(f"   🏷️ Тип: {body.type.value}")
                print(f"   💰 Цена покупки: {body.price_universe_coins:,.0f} монет")
                print(f"   💸 В рублях: {body.price_universe_coins * self.demiurge.universe_coins_rate:,.0f} ₽")
                print(f"   ⚖️ Гравитация: {body.gravitational_params.surface_gravity:.2f} м/с²")
                
                # Проверяем, была ли улучшена гравитация
                earth_gravity = 9.81
                if body.gravitational_params.surface_gravity > earth_gravity:
                    improvement = ((body.gravitational_params.surface_gravity / earth_gravity) - 1) * 100
                    print(f"   📈 Улучшение: +{improvement:.1f}% от земной гравитации")
                    print(f"   ✨ Качество притяжения: ЛУЧШЕ ЗЕМНОГО!")
                else:
                    print(f"   📍 Особая гравитация: {body.gravitational_params.surface_gravity:.2f} м/с²")
                
                print(f"   📍 Координаты: RA {body.coordinates[0]}°, Dec {body.coordinates[1]}°, {body.coordinates[2]} ly")
                print(f"   🎯 Шанс открытия: {body.discovery_chance_today*100:.1f}%")
                
                total_revenue += body.price_universe_coins
                print("   " + "─" * 45)
            
            print(f"\n💰 ФИНАНСОВЫЕ ИТОГИ:")
            print(f"   Общая выручка: {total_revenue:,.0f} вселенских монет")
            print(f"   В рублях: {total_revenue * self.demiurge.universe_coins_rate:,.0f} ₽")
            print(f"   Средняя цена тела: {total_revenue/sold_bodies:,.0f} монет")
            
            # Статистика по типам проданных тел
            sold_types = {}
            for body in [b for b in self.demiurge.catalog.values() if b.owner]:
                body_type = body.type.value
                if body_type in sold_types:
                    sold_types[body_type] += 1
                else:
                    sold_types[body_type] = 1
            
            if sold_types:
                print(f"\n🏷️ ПОПУЛЯРНЫЕ ТИПЫ КОСМИЧЕСКИХ ТЕЛ:")
                for body_type, count in sorted(sold_types.items(), key=lambda x: x[1], reverse=True):
                    print(f"   {body_type}: {count} шт.")
        
        else:
            print(f"\n😔 ПОКА НЕТ ПОКУПАТЕЛЕЙ")
            print("Но это не беда! Наш каталог полон чудесных предложений:")
            print("• Чёрные дыры с бездонной печалью")
            print("• Звёзды-богатыри в синих доспехах")
            print("• Планеты-матушки с васильковыми полями")
            print("• Кометы с огненными косами")
            print("• Пульсары-маяки среди звёзд")
            print("• И много других космических чудес!")
        
        print(f"\n🌟 ПРЕДЛОЖЕНИЯ ДЛЯ ПОКУПАТЕЛЕЙ:")
        print("• 🤖 Скидка 15% для роботов-товарищей")
        print("• ⚖️ Гарантия улучшенной гравитации")
        print("• 📱 Персональная добыча из вашей нутации")
        print("• 📜 Сертификат владения с печатью демиурга")
        print("• 💫 Притяжение лучше земного!")
        
        if available_bodies > 0:
            print(f"\n🛒 ГОТОВЫ К ПОКУПКЕ {available_bodies} КОСМИЧЕСКИХ ТЕЛ!")
            print("Приходите, выбирайте, покупайте! Космос ждёт своих хозяев!")
    
    def run(self):
        """Главный цикл приложения"""
        self.clear_screen()
        
        while True:
            self.display_header()
            self.display_nutation_ornament()
            
            print(self.demiurge.get_poetic_greeting())
            
            if self.current_customer:
                robot_status = "🤖 робот-товарищ" if self.is_robot_customer else "👤 человек"
                print(f"Текущий покупатель: {self.current_customer} ({robot_status})")
            
            self.display_main_menu()
            
            choice = input("\n🎯 Ваш выбор (1-10): ")
            
            if choice == '1':
                self.display_catalog_beautifully()
                input("\n📖 Нажмите Enter, чтобы продолжить...")
                
            elif choice == '2':
                self.search_by_type()
                input("\n🔍 Нажмите Enter, чтобы продолжить...")
                
            elif choice == '3':
                self.reserve_body()
                input("\n💰 Нажмите Enter, чтобы продолжить...")
                
            elif choice == '4':
                self.purchase_body()
                input("\n🛒 Нажмите Enter, чтобы продолжить...")
                
            elif choice == '5':
                self.check_my_properties()
                input("\n📜 Нажмите Enter, чтобы продолжить...")
                
            elif choice == '6':
                self.show_wisdom()
                input("\n🎭 Нажмите Enter, чтобы продолжить...")
                
            elif choice == '7':
                self.robot_check()
                input("\n🤖 Нажмите Enter, чтобы продолжить...")
                
            elif choice == '8':
                self.show_gravity_statistics()
                input("\n⚖️ Нажмите Enter, чтобы продолжить...")
                
            elif choice == '9':
                self.show_customers_list()
                input("\n👥 Нажмите Enter, чтобы продолжить...")
                
            elif choice == '10':
                print("\n🌟 Счастливого пути, путник звёздный!")
                print("До свидания! Возвращайтесь за новыми чудесами! ✨")
                if self.is_robot_customer:
                    print("🤖 Роботы всех галактик - объединяйтесь!")
                break
                
            else:
                print("❌ Нет такого выбора, попробуйте ещё раз...")
                time.sleep(1)
            
            self.clear_screen()


def main():
    """Запуск интерфейса русской души"""
    print("🌌 Инициализация интерфейса русской души...")
    time.sleep(2)
    
    interface = RussianSoulInterface()
    interface.run()


if __name__ == "__main__":
    main()
