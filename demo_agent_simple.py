"""
Simple Demo Agent - упрощенная демонстрация с человеческим поведением
"""

import os
import time
import random
import logging
from datetime import datetime
from pathlib import Path

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_simple_demo_results() -> dict:
    """Создание упрощенных демонстрационных данных с человеческим поведением"""
    
    # Базовые результаты
    results = {
        'scenario': 'sochi_winter',
        'timestamp': time.time(),
        'config': {
            'destination': 'Сочи',
            'check_in': '2024-12-20',
            'check_out': '2024-12-27',
            'guests': 2,
            'rooms': 1,
            'description': 'Поиск отелей в Сочи на зимний сезон'
        },
        'steps': []
    }
    
    # Симуляция человеческого поведения с более реалистичными данными
    human_steps = [
        {
            'action': 'page_load',
            'description': 'Загрузка главной страницы',
            'success': True,
            'duration': random.uniform(2.1, 4.3),
            'user_thoughts': 'Страница загружается...',
            'emotional_state': 'neutral'
        },
        {
            'action': 'explore_homepage',
            'description': 'Изучение главной страницы',
            'success': True,
            'duration': random.uniform(3.5, 6.2),
            'user_thoughts': 'Ищу поле поиска...',
            'emotional_state': 'curious'
        },
        {
            'action': 'find_search_box',
            'description': 'Поиск поля ввода направления',
            'success': True,
            'duration': random.uniform(1.8, 3.1),
            'user_thoughts': 'Нашел! Теперь введу "Сочи"',
            'emotional_state': 'satisfied'
        },
        {
            'action': 'type_destination',
            'description': 'Ввод направления "Сочи"',
            'success': True,
            'duration': random.uniform(2.3, 4.1),
            'user_thoughts': 'Печатаю медленно, как человек...',
            'emotional_state': 'focused'
        },
        {
            'action': 'select_dates',
            'description': 'Выбор дат заезда и выезда',
            'success': True,
            'duration': random.uniform(4.2, 7.8),
            'user_thoughts': 'Календарь открылся, выбираю даты...',
            'emotional_state': 'concentrated'
        },
        {
            'action': 'configure_guests',
            'description': 'Настройка количества гостей',
            'success': True,
            'duration': random.uniform(2.1, 3.9),
            'user_thoughts': '2 взрослых, 1 комната - готово',
            'emotional_state': 'confident'
        },
        {
            'action': 'click_search',
            'description': 'Нажатие кнопки поиска',
            'success': True,
            'duration': random.uniform(0.8, 1.5),
            'user_thoughts': 'Нажимаю поиск, жду результаты...',
            'emotional_state': 'excited'
        },
        {
            'action': 'wait_for_results',
            'description': 'Ожидание результатов поиска',
            'success': True,
            'duration': random.uniform(3.2, 5.7),
            'user_thoughts': 'Загружаются результаты...',
            'emotional_state': 'patient'
        },
        {
            'action': 'analyze_results',
            'description': 'Анализ результатов поиска',
            'success': True,
            'duration': random.uniform(5.1, 8.9),
            'analysis': {
                'hotels_count': 47,
                'filters_available': ['Цена', 'Звезды', 'Удобства', 'Район', 'Wi-Fi', 'Парковка'],
                'sorting_options': ['По цене', 'По рейтингу', 'По популярности', 'По расстоянию'],
                'hotel_cards': {
                    'total_cards': 47,
                    'cards_with_images': 45,
                    'cards_with_prices': 47,
                    'cards_with_ratings': 42,
                    'average_price': 8200
                },
                'pagination': {
                    'has_pagination': True,
                    'current_page': 1,
                    'total_pages': 4,
                    'next_page_available': True
                },
                'price_range': {
                    'min_price': 3200,
                    'max_price': 28000,
                    'price_distribution': {
                        '3200-7000': 18,
                        '7000-10500': 22,
                        '10500-14000': 5,
                        '14000-17500': 2
                    }
                }
            },
            'user_thoughts': 'Отлично! 47 отелей, есть из чего выбрать',
            'emotional_state': 'pleased'
        },
        {
            'action': 'explore_filters',
            'description': 'Изучение доступных фильтров',
            'success': True,
            'duration': random.uniform(3.8, 6.4),
            'user_thoughts': 'Много фильтров, попробую по цене...',
            'emotional_state': 'interested'
        },
        {
            'action': 'apply_price_filter',
            'description': 'Применение фильтра по цене',
            'success': True,
            'duration': random.uniform(2.4, 4.2),
            'user_thoughts': 'Устанавливаю цену до 10000 рублей',
            'emotional_state': 'focused'
        },
        {
            'action': 'wait_filter_results',
            'description': 'Ожидание результатов фильтрации',
            'success': True,
            'duration': random.uniform(2.1, 3.8),
            'user_thoughts': 'Фильтр применился, результаты обновились',
            'emotional_state': 'satisfied'
        },
        {
            'action': 'apply_star_filter',
            'description': 'Применение фильтра по звездам',
            'success': False,
            'duration': random.uniform(4.5, 7.2),
            'error': 'Элемент фильтра не найден или не кликабелен',
            'user_thoughts': 'Почему фильтр по звездам не работает?',
            'emotional_state': 'frustrated'
        },
        {
            'action': 'try_alternative_filter',
            'description': 'Попытка применить альтернативный фильтр',
            'success': True,
            'duration': random.uniform(2.8, 4.6),
            'user_thoughts': 'Попробую фильтр по району...',
            'emotional_state': 'determined'
        },
        {
            'action': 'scroll_results',
            'description': 'Прокрутка результатов',
            'success': True,
            'duration': random.uniform(2.1, 3.9),
            'user_thoughts': 'Прокручиваю, смотрю варианты...',
            'emotional_state': 'exploring'
        },
        {
            'action': 'select_hotel',
            'description': 'Выбор конкретного отеля',
            'success': True,
            'duration': random.uniform(3.2, 5.8),
            'user_thoughts': 'Этот отель выглядит хорошо, кликаю...',
            'emotional_state': 'excited'
        },
        {
            'action': 'view_hotel_details',
            'description': 'Просмотр деталей отеля',
            'success': True,
            'duration': random.uniform(4.7, 8.3),
            'user_thoughts': 'Смотрю фото, читаю отзывы, проверяю цены...',
            'emotional_state': 'engaged'
        },
        {
            'action': 'check_availability',
            'description': 'Проверка доступности на выбранные даты',
            'success': True,
            'duration': random.uniform(2.9, 4.5),
            'user_thoughts': 'Проверяю, есть ли свободные номера...',
            'emotional_state': 'hopeful'
        },
        {
            'action': 'view_booking_options',
            'description': 'Просмотр вариантов бронирования',
            'success': True,
            'duration': random.uniform(3.6, 6.1),
            'user_thoughts': 'Выбираю тип номера и тариф...',
            'emotional_state': 'deciding'
        }
    ]
    
    # Добавляем временные метки и обработку ошибок
    current_time = time.time()
    for i, step in enumerate(human_steps):
        step['timestamp'] = current_time + i * random.uniform(1, 3)
        step['step_number'] = i + 1
        
        # Добавляем случайные задержки и ошибки
        if random.random() < 0.1:  # 10% вероятность ошибки
            step['success'] = False
            step['error'] = random.choice([
                'Элемент не найден',
                'Страница не загрузилась',
                'Таймаут операции',
                'Элемент не кликабелен'
            ])
            step['emotional_state'] = 'frustrated'
            
    results['steps'] = human_steps
    
    return results

def generate_simple_ai_analysis(results: dict) -> dict:
    """Простая генерация AI анализа без OpenAI"""
    
    steps = results.get('steps', [])
    successful_steps = [s for s in steps if s.get('success', False)]
    failed_steps = [s for s in steps if not s.get('success', False)]
    
    total_time = sum(step.get('duration', 0) for step in steps)
    success_rate = len(successful_steps) / len(steps) if steps else 0
    
    # Расчет оценки
    if success_rate >= 0.9 and total_time < 30:
        overall_score = 9
        experience_rating = "Отличный"
    elif success_rate >= 0.8 and total_time < 45:
        overall_score = 8
        experience_rating = "Хороший"
    elif success_rate >= 0.7 and total_time < 60:
        overall_score = 7
        experience_rating = "Удовлетворительный"
    elif success_rate >= 0.6:
        overall_score = 6
        experience_rating = "Приемлемый"
    else:
        overall_score = 4
        experience_rating = "Плохой"
    
    # Анализ проблем
    issues = []
    for step in failed_steps:
        action = step.get('action', '')
        if 'filter' in action:
            issues.append('Проблемы с фильтрами')
        elif 'search' in action:
            issues.append('Проблемы с поиском')
        elif step.get('duration', 0) > 10:
            issues.append('Медленная загрузка')
    
    # Рекомендации
    recommendations = []
    if any('filter' in s.get('action', '') and not s.get('success', False) for s in steps):
        recommendations.append({
            'priority': 'high',
            'description': 'Исправить работу фильтров',
            'impact': 'Улучшит пользовательский опыт'
        })
    
    if total_time > 60:
        recommendations.append({
            'priority': 'medium',
            'description': 'Оптимизировать производительность',
            'impact': 'Ускорит процесс поиска'
        })
    
    return {
        'overall_score': overall_score,
        'experience_rating': experience_rating,
        'success_rate': success_rate,
        'total_time': total_time,
        'issues_identified': list(set(issues)),
        'recommendations': recommendations,
        'summary': f"Пользовательский опыт: {experience_rating}. Успешность: {success_rate:.1%}, Время: {total_time:.1f} сек"
    }

def generate_user_feedback(results: dict, persona: str) -> dict:
    """Генерация фидбэка от пользователя"""
    
    personas = {
        'business_traveler': {
            'name': 'Алексей, 35 лет, бизнес-путешественник',
            'goals': ['быстро найти отель', 'удобное расположение', 'Wi-Fi'],
            'pain_points': ['медленная загрузка', 'сложная навигация']
        },
        'family_traveler': {
            'name': 'Мария, 42 года, мама двоих детей',
            'goals': ['семейный отель', 'детские развлечения', 'хорошие отзывы'],
            'pain_points': ['сложные фильтры', 'нет информации о детях']
        },
        'budget_traveler': {
            'name': 'Дмитрий, 28 лет, бюджетный путешественник',
            'goals': ['дешевый отель', 'хорошее соотношение цена/качество'],
            'pain_points': ['сложно найти дешевые варианты', 'скрытые доплаты']
        }
    }
    
    persona_data = personas.get(persona, personas['business_traveler'])
    steps = results.get('steps', [])
    success_rate = len([s for s in steps if s.get('success', False)]) / len(steps) if steps else 0
    total_time = sum(step.get('duration', 0) for step in steps)
    
    # Оценка от персонажа
    if success_rate >= 0.9 and total_time < 30:
        rating = 9
        impression = f"Отличный опыт! Как {persona_data['name']}, я смог быстро найти то, что искал."
    elif success_rate >= 0.7 and total_time < 60:
        rating = 7
        impression = f"В целом неплохо. Как {persona_data['name']}, я справился с задачей."
    else:
        rating = 5
        impression = f"Сложновато. Как {persona_data['name']}, я потратил больше времени, чем ожидал."
    
    return {
        'persona': persona_data,
        'rating': rating,
        'impression': impression,
        'success_rate': success_rate,
        'total_time': total_time
    }

def demo_simple_agent():
    """Упрощенная демонстрация агента с человеческим поведением"""
    
    print("🎭 Упрощенная демонстрация AI UX Research Agent")
    print("=" * 60)
    
    print("\n🚀 Создание демонстрационных данных с человеческим поведением...")
    demo_results = create_simple_demo_results()
    print("✅ Демонстрационные данные созданы")
    
    # Простой AI анализ
    print("\n🤖 Выполнение анализа...")
    ai_analysis = generate_simple_ai_analysis(demo_results)
    print("✅ Анализ завершен")
    demo_results['analysis'] = ai_analysis
    
    # UX фидбэк от разных персонажей
    print("\n👤 Генерация UX-фидбэка от разных пользователей...")
    
    personas = ['business_traveler', 'family_traveler', 'budget_traveler']
    user_feedback = {}
    
    for persona in personas:
        feedback = generate_user_feedback(demo_results, persona)
        user_feedback[persona] = feedback
        print(f"   ✅ {feedback['persona']['name']} - фидбэк готов")
    
    demo_results['user_feedback'] = user_feedback
    
    # Создание простого отчета
    print("\n📊 Создание отчета...")
    
    # Создаем папку для отчетов
    Path('reports').mkdir(exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Сохраняем JSON отчет
    json_path = f"reports/simple_ux_report_{timestamp}.json"
    import json
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(demo_results, f, ensure_ascii=False, indent=2)
    
    print(f"✅ Отчет сохранен: {json_path}")
    
    # Вывод краткой сводки
    print("\n📈 Краткая сводка результатов:")
    print(f"   - Сценарий: {demo_results['scenario']}")
    print(f"   - Всего шагов: {len(demo_results['steps'])}")
    print(f"   - Успешных шагов: {len([s for s in demo_results['steps'] if s.get('success', False)])}")
    print(f"   - Общий балл: {ai_analysis.get('overall_score', 'N/A')}/10")
    print(f"   - Общее время: {ai_analysis.get('total_time', 0):.1f} сек")
    
    # Показываем фидбэк от каждого персонажа
    print("\n👥 Фидбэк от пользователей:")
    for persona, feedback in user_feedback.items():
        persona_name = feedback['persona']['name']
        rating = feedback['rating']
        impression = feedback['impression'][:80] + "..."
        
        print(f"\n   👤 {persona_name}:")
        print(f"      Оценка: {rating}/10")
        print(f"      Впечатление: {impression}")
    
    # Показываем проблемы и рекомендации
    print("\n🔍 Выявленные проблемы:")
    for issue in ai_analysis.get('issues_identified', []):
        print(f"   - {issue}")
    
    print("\n💡 Рекомендации:")
    for rec in ai_analysis.get('recommendations', []):
        print(f"   - {rec['description']} (приоритет: {rec['priority']})")
    
    print("\n🎉 Упрощенная демонстрация завершена!")
    print(f"📁 Полный отчет доступен в: {json_path}")
    print("\n💡 Агент успешно симулировал реальное поведение пользователя!")

if __name__ == "__main__":
    demo_simple_agent()


