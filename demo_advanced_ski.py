"""
Demo Advanced Ski - демонстрация расширенного горнолыжного сценария
"""

import os
import time
import random
import logging
from datetime import datetime
from pathlib import Path

from config.advanced_scenarios import get_advanced_scenarios, get_ski_personas, get_enhanced_search_prompt

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_advanced_ski_results(scenario_name: str) -> dict:
    """Создание результатов для расширенного горнолыжного сценария"""
    
    scenarios = get_advanced_scenarios()
    scenario = scenarios.get(scenario_name, {})
    
    if not scenario:
        print(f"❌ Сценарий {scenario_name} не найден")
        return {}
    
    requirements = scenario.get('requirements', {})
    
    # Создаем расширенные шаги с учетом горнолыжных требований
    advanced_steps = [
        {
            'action': 'page_load',
            'description': 'Загрузка главной страницы',
            'success': True,
            'duration': random.uniform(2.1, 4.3),
            'user_thoughts': 'Открываю сайт для поиска горнолыжного отеля...',
            'emotional_state': 'excited'
        },
        {
            'action': 'search_destination',
            'description': f'Поиск направления: {scenario["destination"]}',
            'success': True,
            'duration': random.uniform(2.3, 4.1),
            'user_thoughts': f'Ищу отели в {scenario["destination"]} для горнолыжного отдыха',
            'emotional_state': 'focused'
        },
        {
            'action': 'select_dates',
            'description': f'Выбор дат: {scenario["check_in"]} - {scenario["check_out"]}',
            'success': True,
            'duration': random.uniform(3.2, 5.8),
            'user_thoughts': 'Выбираю даты для зимнего горнолыжного отдыха',
            'emotional_state': 'concentrated'
        },
        {
            'action': 'apply_star_filter',
            'description': f'Фильтр по звездам: {requirements.get("stars", "Любые")}',
            'success': True,
            'duration': random.uniform(2.1, 3.9),
            'user_thoughts': f'Устанавливаю фильтр {requirements.get("stars", "Любые")}',
            'emotional_state': 'focused'
        },
        {
            'action': 'apply_price_filter',
            'description': f'Фильтр по цене: {requirements.get("price_limit", "Любая")}',
            'success': True,
            'duration': random.uniform(2.4, 4.2),
            'user_thoughts': f'Устанавливаю лимит цены {requirements.get("price_limit", "Любая")}',
            'emotional_state': 'determined'
        },
        {
            'action': 'search_ski_facilities',
            'description': 'Поиск горнолыжных удобств',
            'success': True,
            'duration': random.uniform(4.1, 6.8),
            'user_thoughts': 'Ищу отели с лыжехранилищем и трансфером к подъемнику',
            'emotional_state': 'interested'
        },
        {
            'action': 'check_distance_to_lift',
            'description': f'Проверка расстояния до подъемника: {requirements.get("distance_to_lift", "Любое")}',
            'success': True,
            'duration': random.uniform(3.5, 5.9),
            'user_thoughts': f'Проверяю, что отель {requirements.get("distance_to_lift", "Любое")}',
            'emotional_state': 'analytical'
        },
        {
            'action': 'check_cancellation_policy',
            'description': f'Проверка условий отмены: {requirements.get("cancellation", "Любая")}',
            'success': True,
            'duration': random.uniform(2.8, 4.6),
            'user_thoughts': f'Проверяю условия отмены - нужна {requirements.get("cancellation", "Любая")}',
            'emotional_state': 'careful'
        },
        {
            'action': 'analyze_ski_results',
            'description': 'Анализ результатов поиска горнолыжных отелей',
            'success': True,
            'duration': random.uniform(5.2, 8.7),
            'analysis': {
                'hotels_count': 23,
                'ski_facilities': {
                    'with_ski_storage': 18,
                    'with_transfer': 15,
                    'ski_in_ski_out': 3,
                    'with_equipment': 8
                },
                'distance_analysis': {
                    'within_1km': 5,
                    'within_2km': 12,
                    'within_5km': 6
                },
                'price_analysis': {
                    'under_5000': 8,
                    'under_10000': 12,
                    'under_25000': 3
                },
                'cancellation_policies': {
                    'free_cancellation': 14,
                    'flexible': 6,
                    'strict': 3
                }
            },
            'user_thoughts': 'Отлично! Нашел 23 отеля с горнолыжными удобствами',
            'emotional_state': 'pleased'
        },
        {
            'action': 'select_best_ski_hotel',
            'description': 'Выбор лучшего горнолыжного отеля',
            'success': True,
            'duration': random.uniform(4.3, 7.1),
            'user_thoughts': 'Выбираю отель, который соответствует всем требованиям',
            'emotional_state': 'excited'
        },
        {
            'action': 'check_ski_services',
            'description': 'Проверка горнолыжных услуг',
            'success': True,
            'duration': random.uniform(3.7, 6.2),
            'user_thoughts': 'Проверяю наличие лыжехранилища, трансфера и других услуг',
            'emotional_state': 'thorough'
        },
        {
            'action': 'verify_cancellation_terms',
            'description': 'Проверка условий отмены бронирования',
            'success': True,
            'duration': random.uniform(2.9, 4.8),
            'user_thoughts': 'Убеждаюсь, что отмена бесплатная до определенной даты',
            'emotional_state': 'satisfied'
        },
        {
            'action': 'final_booking_decision',
            'description': 'Финальное решение о бронировании',
            'success': True,
            'duration': random.uniform(3.1, 5.4),
            'user_thoughts': 'Отель идеально подходит! Могу бронировать',
            'emotional_state': 'confident'
        }
    ]
    
    # Добавляем временные метки
    current_time = time.time()
    for i, step in enumerate(advanced_steps):
        step['timestamp'] = current_time + i * random.uniform(1, 3)
        step['step_number'] = i + 1
    
    return {
        'scenario': scenario_name,
        'timestamp': time.time(),
        'config': {
            'destination': scenario['destination'],
            'check_in': scenario['check_in'],
            'check_out': scenario['check_out'],
            'guests': scenario['guests'],
            'rooms': scenario['rooms'],
            'description': scenario['description'],
            'requirements': requirements
        },
        'steps': advanced_steps
    }

def demo_advanced_ski_scenario():
    """Демонстрация расширенного горнолыжного сценария"""
    
    print("🎿 ДЕМОНСТРАЦИЯ РАСШИРЕННОГО ГОРНОЛЫЖНОГО СЦЕНАРИЯ")
    print("=" * 70)
    
    # Показываем доступные сценарии
    scenarios = get_advanced_scenarios()
    print(f"\n📋 ДОСТУПНЫЕ СЦЕНАРИИ:")
    for key, scenario in scenarios.items():
        print(f"   • {key}: {scenario['name']}")
    
    # Выбираем сценарий
    scenario_name = 'sochi_ski_premium'
    print(f"\n🎯 ВЫБРАН СЦЕНАРИЙ: {scenario_name}")
    
    # Показываем расширенный промпт
    prompt = get_enhanced_search_prompt(scenario_name)
    print(f"\n📝 РАСШИРЕННЫЙ ПРОМПТ:")
    print(prompt)
    
    # Создаем результаты
    print(f"\n🚀 СОЗДАНИЕ РЕЗУЛЬТАТОВ...")
    results = create_advanced_ski_results(scenario_name)
    
    if not results:
        print("❌ Ошибка создания результатов")
        return
    
    print(f"✅ Результаты созданы")
    
    # Показываем статистику
    steps = results.get('steps', [])
    successful_steps = [s for s in steps if s.get('success', False)]
    
    print(f"\n📊 СТАТИСТИКА:")
    print(f"   Всего шагов: {len(steps)}")
    print(f"   Успешных шагов: {len(successful_steps)}")
    print(f"   Успешность: {len(successful_steps)/len(steps)*100:.1f}%")
    
    # Показываем ключевые шаги
    print(f"\n🔍 КЛЮЧЕВЫЕ ШАГИ:")
    for step in steps:
        if any(keyword in step.get('action', '') for keyword in ['ski', 'lift', 'cancellation', 'price']):
            print(f"   ✅ {step.get('description', '')}")
    
    # Показываем анализ результатов
    for step in steps:
        if step.get('action') == 'analyze_ski_results':
            analysis = step.get('analysis', {})
            print(f"\n📈 АНАЛИЗ РЕЗУЛЬТАТОВ:")
            print(f"   Найдено отелей: {analysis.get('hotels_count', 0)}")
            print(f"   С лыжехранилищем: {analysis.get('ski_facilities', {}).get('with_ski_storage', 0)}")
            print(f"   С трансфером: {analysis.get('ski_facilities', {}).get('with_transfer', 0)}")
            print(f"   В пределах 2 км: {analysis.get('distance_analysis', {}).get('within_2km', 0)}")
            print(f"   С бесплатной отменой: {analysis.get('cancellation_policies', {}).get('free_cancellation', 0)}")
            break
    
    # Показываем персонажи
    personas = get_ski_personas()
    scenario = scenarios.get(scenario_name, {})
    persona_key = scenario.get('persona', 'ski_enthusiast')
    persona = personas.get(persona_key, {})
    
    print(f"\n👤 ПЕРСОНАЖ: {persona.get('name', 'Неизвестно')}")
    print(f"   Цели: {', '.join(persona.get('goals', []))}")
    print(f"   Приоритеты: {', '.join(persona.get('priorities', []))}")
    print(f"   Типичная оценка: {persona.get('typical_rating', 'N/A')}")
    
    print(f"\n🎉 ДЕМОНСТРАЦИЯ ЗАВЕРШЕНА!")
    print(f"💡 Расширенный сценарий учитывает все ваши требования!")
    print(f"💡 Система может анализировать специфичные горнолыжные потребности!")

if __name__ == "__main__":
    demo_advanced_ski_scenario()


