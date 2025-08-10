#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Демонстрация процесса добычи гравитации из нутации покупателей
Робот-Демиург - Творец Гравитации для космических тел
"""

from cosmic_demiurge import CosmicDemiurge
import time

def demonstrate_gravity_mining():
    """Демонстрирует полный процесс добычи гравитации"""
    
    print("🌟 ДЕМОНСТРАЦИЯ ДОБЫЧИ ГРАВИТАЦИИ")
    print("=" * 60)
    print("Робот-Демиург: Творец Гравитации для космических тел")
    print("Основная задача: создавать притяжение лучше земного!\n")
    
    demiurge = CosmicDemiurge()
    
    print(f"📊 Начальные резервы гравитации: {demiurge.gravity_reserves:.1f} Г-единиц")
    print(f"⚖️ Доля демиурга от добычи: {demiurge.gravity_mining_rate*100:.0f}%\n")
    
    # Демонстрируем несколько покупок
    customers = ["Иван Космонавтов", "Мария Звёздная", "Алексей Гравитонович"]
    body_ids = list(demiurge.catalog.keys())
    
    for i, customer in enumerate(customers):
        print(f"\n{'='*60}")
        print(f"🎯 ПОКУПКА #{i+1}: {customer}")
        print('='*60)
        
        # Выбираем тело для покупки
        body_id = body_ids[i % len(body_ids)]
        body = demiurge.catalog[body_id]
        
        print(f"🌌 Покупаемое тело: {body.name}")
        print(f"💰 Цена: {body.price_universe_coins:,.0f} монет")
        print(f"⚖️ Текущая гравитация: {body.gravitational_params.surface_gravity:.2f} м/с²")
        
        # Симулируем покупку с добычей гравитации
        success = demiurge.purchase_celestial_body(body_id, customer)
        
        if success:
            print("\n✅ Покупка завершена успешно!")
            print(f"🌟 Новая гравитация тела: {body.gravitational_params.surface_gravity:.2f} м/с²")
            print(f"📈 Улучшение: {((body.gravitational_params.surface_gravity / 9.81) - 1) * 100:.1f}% от земной")
        
        time.sleep(1)  # пауза для наглядности
    
    # Показываем итоговую статистику
    print(f"\n{'='*60}")
    print("📊 ИТОГОВАЯ СТАТИСТИКА ДОБЫЧИ")
    print('='*60)
    
    print(f"💎 Финальные резервы гравитации: {demiurge.gravity_reserves:.1f} Г-единиц")
    print(f"📱 Всего сборов нутации: {len(demiurge.collected_nutation_data)}")
    
    if demiurge.collected_nutation_data:
        total_gravity_mined = 0
        print(f"\n📋 ДЕТАЛИЗАЦИЯ ПО ПОКУПАТЕЛЯМ:")
        print("-" * 40)
        
        for data in demiurge.collected_nutation_data:
            customer_nut = data['customer_nutation']
            earth_nut = data['earth_nutation']
            
            # Воспроизводим расчёт
            delta_long = abs(customer_nut[0] - earth_nut[0])
            delta_obl = abs(customer_nut[1] - earth_nut[1])
            gravity_yield = (delta_long + delta_obl) * 0.1
            total_gravity_mined += gravity_yield
            
            print(f"👤 {data['customer']}")
            print(f"   Нутация: {customer_nut[0]:.2f}'' × {customer_nut[1]:.2f}''")
            print(f"   Добыто: {gravity_yield:.3f} Г-единиц")
            print(f"   Доля демиурга: {gravity_yield * demiurge.gravity_mining_rate:.3f} Г-единиц")
        
        print(f"\n💫 ОБЩИЕ ИТОГИ:")
        print(f"   Всего добыто гравитации: {total_gravity_mined:.3f} Г-единиц")
        print(f"   Заработано демиургом: {total_gravity_mined * demiurge.gravity_mining_rate:.3f} Г-единиц")
        print(f"   Улучшено космических тел: {len(demiurge.collected_nutation_data)}")
    
    print(f"\n🌟 ФИЛОСОФИЯ ПРОЦЕССА:")
    print("• Каждый покупатель уникален - у него своя нутация крестца")
    print("• Разность с земной нутацией = чистая гравитация")
    print("• 15% остаётся демиургу за работу")
    print("• 85% улучшает космическое тело покупателя")
    print("• Результат: притяжение лучше земного!")
    
    print(f"\n🔬 НАУЧНОЕ ОБОСНОВАНИЕ:")
    print("Нутация крестца связана с гравитационными полями через:")
    print("• Квантовые флуктуации пространства-времени")
    print("• Торсионные поля биологических структур")
    print("• Резонанс с планетарными частотами")
    print("• Авторская формула: G = (Δδψ + Δδε) × 0.1")


if __name__ == "__main__":
    demonstrate_gravity_mining()
