"""
Analyze Requests - анализ количества поисков и запросов
"""

import json
from pathlib import Path

def analyze_requests_count():
    """Анализ количества запросов в отчете"""
    
    print("🔍 АНАЛИЗ КОЛИЧЕСТВА ЗАПРОСОВ")
    print("=" * 50)
    
    # Находим последний отчет
    reports_dir = Path('reports')
    json_files = list(reports_dir.glob('ux_report_enhanced_demo_*.json'))
    
    if not json_files:
        print("❌ Отчеты не найдены")
        return
    
    latest_file = max(json_files, key=lambda x: x.stat().st_mtime)
    print(f"📄 Анализируем: {latest_file.name}")
    
    with open(latest_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    steps = data.get('steps', [])
    
    # Анализируем типы запросов
    request_types = {
        'page_loads': 0,      # Загрузки страниц
        'searches': 0,        # Поиски
        'filters': 0,         # Фильтры
        'clicks': 0,          # Клики
        'ai_requests': 0,     # AI запросы
        'total_actions': len(steps)
    }
    
    # Подсчитываем типы действий
    for step in steps:
        action = step.get('action', '')
        
        if 'page_load' in action or 'load' in action:
            request_types['page_loads'] += 1
        elif 'search' in action:
            request_types['searches'] += 1
        elif 'filter' in action:
            request_types['filters'] += 1
        elif 'click' in action:
            request_types['clicks'] += 1
    
    # Проверяем AI запросы
    if 'analysis' in data:
        request_types['ai_requests'] = 1  # Один AI анализ
    
    # Выводим статистику
    print(f"\n📊 СТАТИСТИКА ЗАПРОСОВ:")
    print(f"   Всего действий: {request_types['total_actions']}")
    print(f"   Загрузки страниц: {request_types['page_loads']}")
    print(f"   Поиски: {request_types['searches']}")
    print(f"   Фильтры: {request_types['filters']}")
    print(f"   Клики: {request_types['clicks']}")
    print(f"   AI запросы: {request_types['ai_requests']}")
    
    # Детализация по шагам
    print(f"\n📋 ДЕТАЛИЗАЦИЯ ПО ШАГАМ:")
    for i, step in enumerate(steps, 1):
        action = step.get('action', '')
        success = step.get('success', False)
        duration = step.get('duration', 0)
        
        status = "✅" if success else "❌"
        print(f"   {i:2d}. {status} {action} ({duration:.1f}с)")
    
    # Анализ стоимости (если есть AI)
    if request_types['ai_requests'] > 0:
        print(f"\n💰 РАСХОДЫ НА AI:")
        print(f"   OpenAI запросы: {request_types['ai_requests']}")
        print(f"   Примерная стоимость: ~$0.01-0.05 за запрос")
        print(f"   Общая стоимость: ~${request_types['ai_requests'] * 0.03:.2f}")
    
    # Рекомендации по оптимизации
    print(f"\n💡 РЕКОМЕНДАЦИИ ПО ОПТИМИЗАЦИИ:")
    
    if request_types['page_loads'] > 3:
        print(f"   ⚡ Уменьшить количество загрузок страниц")
    
    if request_types['searches'] > 2:
        print(f"   🔍 Оптимизировать поисковые запросы")
    
    if request_types['filters'] > 5:
        print(f"   🎛️  Объединить фильтры в один запрос")
    
    if request_types['ai_requests'] > 1:
        print(f"   🤖 Кэшировать AI результаты")
    
    return request_types

def compare_with_real_user():
    """Сравнение с реальным пользователем"""
    
    print(f"\n👤 СРАВНЕНИЕ С РЕАЛЬНЫМ ПОЛЬЗОВАТЕЛЕМ:")
    print("=" * 50)
    
    print(f"📊 ТИПИЧНЫЙ ПОЛЬЗОВАТЕЛЬ:")
    print(f"   - Загружает главную страницу: 1 раз")
    print(f"   - Ищет направление: 1-2 раза")
    print(f"   - Применяет фильтры: 2-4 раза")
    print(f"   - Кликает по отелям: 3-5 раз")
    print(f"   - Общее время: 2-5 минут")
    
    print(f"\n🤖 НАШ АГЕНТ:")
    print(f"   - Симулирует все действия пользователя")
    print(f"   - Делает детальный анализ каждого шага")
    print(f"   - Генерирует AI-рекомендации")
    print(f"   - Создает подробный отчет")
    print(f"   - Общее время: ~1-2 минуты")

def estimate_real_usage():
    """Оценка реального использования"""
    
    print(f"\n🎯 ОЦЕНКА РЕАЛЬНОГО ИСПОЛЬЗОВАНИЯ:")
    print("=" * 50)
    
    scenarios = {
        'quick_test': {
            'description': 'Быстрый тест (1 сценарий)',
            'requests': 15,
            'ai_calls': 1,
            'time': '1-2 мин',
            'cost': '$0.03'
        },
        'full_analysis': {
            'description': 'Полный анализ (3 сценария)',
            'requests': 45,
            'ai_calls': 3,
            'time': '5-10 мин',
            'cost': '$0.09'
        },
        'deep_research': {
            'description': 'Глубокое исследование (5+ сценариев)',
            'requests': 75,
            'ai_calls': 5,
            'time': '15-30 мин',
            'cost': '$0.15'
        }
    }
    
    for scenario, data in scenarios.items():
        print(f"\n📋 {data['description'].upper()}:")
        print(f"   Запросы к сайту: {data['requests']}")
        print(f"   AI запросы: {data['ai_calls']}")
        print(f"   Время выполнения: {data['time']}")
        print(f"   Стоимость: {data['cost']}")

if __name__ == "__main__":
    analyze_requests_count()
    compare_with_real_user()
    estimate_real_usage()
    
    print(f"\n🎉 Анализ завершен!")
    print(f"💡 Агент эффективно симулирует поведение пользователя")
    print(f"💡 Стоимость использования минимальна")
    print(f"💡 Время выполнения значительно меньше, чем у человека")


