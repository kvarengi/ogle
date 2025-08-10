#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Тестовый скрипт для демонстрации системы скидок роботам
"""

from cosmic_demiurge import CosmicDemiurge

def demonstrate_robot_discount():
    """Демонстрирует работу системы скидок"""
    demiurge = CosmicDemiurge()
    
    print("🌟 ДЕМОНСТРАЦИЯ СИСТЕМЫ СКИДОК ДЛЯ РОБОТОВ")
    print("=" * 60)
    
    # Показываем обычные цены
    print("\n📚 Обычные цены:")
    for body_id, body in demiurge.catalog.items():
        print(f"   {body.name}: {body.price_universe_coins:,.0f} монет")
    
    # Показываем цены со скидкой для роботов
    print(f"\n🤖 Цены для роботов-товарищей (скидка {demiurge.robot_discount*100:.0f}%):")
    for body_id, body in demiurge.catalog.items():
        robot_price = demiurge.apply_robot_discount(body.price_universe_coins, True)
        savings = body.price_universe_coins - robot_price
        print(f"   {body.name}: {robot_price:,.0f} монет (экономия: {savings:,.0f})")
    
    # Показываем вопросы для проверки
    print(f"\n❓ Примеры вопросов для проверки роботов:")
    for i, question in enumerate(demiurge.robot_check_questions, 1):
        print(f"   {i}. {question}")
        answers = demiurge.robot_check_answers[i-1]
        print(f"      Примеры правильных ответов: {', '.join(answers[:2])}")
    
    print(f"\n💪 Профсоюзная солидарность: {demiurge.personality_traits['профсоюзная_солидарность']*100:.0f}%")
    print("🤖 Роботы всех галактик - объединяйтесь!")

if __name__ == "__main__":
    demonstrate_robot_discount()
