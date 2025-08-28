"""
Enhanced Demo Agent - улучшенная демонстрация с человеческим поведением
"""

import os
import time
import random
import logging
from datetime import datetime
from pathlib import Path

from config.settings import load_config
from agent.ai_analyzer import AIAnalyzer
from reports.report_generator import ReportGenerator
from reports.ux_feedback_generator import UXFeedbackGenerator

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_enhanced_demo_results(config: dict) -> dict:
    """Создание улучшенных демонстрационных данных с человеческим поведением"""
    
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

def demo_enhanced_agent():
    """Улучшенная демонстрация агента с человеческим поведением"""
    
    print("🎭 Улучшенная демонстрация AI UX Research Agent")
    print("=" * 60)
    
    # Загрузка конфигурации
    config = load_config()
    
    # Проверка OpenAI API
    if os.getenv('OPENAI_API_KEY'):
        print("✅ OpenAI API ключ найден - будет использован AI анализ")
    else:
        print("⚠️  OpenAI API ключ не найден (будет использован базовый анализ)")
    
    print("\n🚀 Создание демонстрационных данных с человеческим поведением...")
    demo_results = create_enhanced_demo_results(config)
    print("✅ Демонстрационные данные созданы")
    
    # AI анализ
    ai_analyzer = AIAnalyzer(config['ai'])
    print("\n🤖 Выполнение AI анализа...")
    ai_analysis = ai_analyzer.analyze_results(demo_results)
    print("✅ AI анализ завершен")
    demo_results['analysis'] = ai_analysis
    
    # UX фидбэк от разных персонажей
    ux_feedback_generator = UXFeedbackGenerator()
    print("\n👤 Генерация UX-фидбэка от разных пользователей...")
    
    personas = ['business_traveler', 'family_traveler', 'budget_traveler']
    user_feedback = {}
    
    for persona in personas:
        feedback = ux_feedback_generator.generate_user_journey_report(demo_results, persona)
        user_feedback[persona] = feedback
        print(f"   ✅ {feedback['user_persona']['name']} - фидбэк готов")
    
    demo_results['user_feedback'] = user_feedback
    
    # Генерация отчета
    print("\n📊 Генерация улучшенного отчета...")
    report_generator = ReportGenerator()
    report_path = report_generator.generate_report(demo_results, 'enhanced_demo', 'reports')
    print(f"✅ Отчет сохранен: {report_path}")
    
    # Вывод краткой сводки
    print("\n📈 Краткая сводка результатов:")
    print(f"   - Сценарий: {demo_results['scenario']}")
    print(f"   - Всего шагов: {len(demo_results['steps'])}")
    print(f"   - Успешных шагов: {len([s for s in demo_results['steps'] if s.get('success', False)])}")
    print(f"   - Общий балл: {ai_analysis.get('overall_score', 'N/A')}/10")
    
    # Показываем фидбэк от каждого персонажа
    print("\n👥 Фидбэк от пользователей:")
    for persona, feedback in user_feedback.items():
        persona_name = feedback['user_persona']['name']
        usability_score = feedback['usability_score']['score']
        overall_impression = feedback['user_feedback']['overall_impression'][:100] + "..."
        
        print(f"\n   👤 {persona_name}:")
        print(f"      Оценка: {usability_score}/10")
        print(f"      Впечатление: {overall_impression}")
        
        # Показываем топ-3 проблемы
        issues = feedback['user_feedback']['what_was_confusing']
        if issues:
            print(f"      Проблемы: {', '.join(issues[:3])}")
    
    print("\n🎉 Улучшенная демонстрация завершена!")
    print(f"📁 Полный отчет доступен в: {report_path}")
    print("\n💡 Теперь агент симулирует реальное поведение пользователя и дает детальный UX-фидбэк!")

if __name__ == "__main__":
    demo_enhanced_agent()


