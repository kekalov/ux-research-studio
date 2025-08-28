"""
Analyze Personas - анализ количества персонажей в отчете
"""

import json
from pathlib import Path

def analyze_personas():
    """Анализ персонажей в отчете"""
    
    print("👥 АНАЛИЗ ПЕРСОНАЖЕЙ В ОТЧЕТЕ")
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
    
    user_feedback = data.get('user_feedback', {})
    
    print(f"\n📊 КОЛИЧЕСТВО ПЕРСОНАЖЕЙ: {len(user_feedback)}")
    
    # Анализируем каждого персонажа
    for persona_key, feedback in user_feedback.items():
        persona = feedback.get('persona', {})
        rating = feedback.get('rating', 0)
        impression = feedback.get('impression', '')
        
        print(f"\n👤 ПЕРСОНАЖ: {persona.get('name', persona_key)}")
        print(f"   Оценка: {rating}/10")
        print(f"   Цели: {', '.join(persona.get('goals', []))}")
        print(f"   Болевые точки: {', '.join(persona.get('pain_points', []))}")
        print(f"   Впечатление: {impression[:100]}...")
    
    # Сравнение оценок
    print(f"\n📈 СРАВНЕНИЕ ОЦЕНОК:")
    ratings = []
    for persona_key, feedback in user_feedback.items():
        persona = feedback.get('persona', {})
        rating = feedback.get('rating', 0)
        ratings.append((persona.get('name', persona_key), rating))
        print(f"   {persona.get('name', persona_key)}: {rating}/10")
    
    # Средняя оценка
    if ratings:
        avg_rating = sum(r[1] for r in ratings) / len(ratings)
        print(f"   Средняя оценка: {avg_rating:.1f}/10")
    
    # Анализ различий
    print(f"\n🔍 АНАЛИЗ РАЗЛИЧИЙ МЕЖДУ ПЕРСОНАЖАМИ:")
    
    if len(ratings) > 1:
        min_rating = min(ratings, key=lambda x: x[1])
        max_rating = max(ratings, key=lambda x: x[1])
        
        print(f"   Самый строгий: {min_rating[0]} ({min_rating[1]}/10)")
        print(f"   Самый лояльный: {max_rating[0]} ({max_rating[1]}/10)")
        print(f"   Разброс оценок: {max_rating[1] - min_rating[1]} баллов")
    
    return user_feedback

def explain_persona_differences():
    """Объяснение различий между персонажами"""
    
    print(f"\n💡 ПОЧЕМУ РАЗНЫЕ ПЕРСОНАЖИ ДАЮТ РАЗНЫЕ ОЦЕНКИ:")
    print("=" * 60)
    
    personas = {
        'business_traveler': {
            'name': 'Алексей, 35 лет, бизнес-путешественник',
            'priorities': ['Скорость', 'Эффективность', 'Надежность'],
            'tolerance': 'Низкая к медленной работе',
            'typical_rating': '6-8/10'
        },
        'family_traveler': {
            'name': 'Мария, 42 года, мама двоих детей',
            'priorities': ['Удобство', 'Безопасность', 'Информативность'],
            'tolerance': 'Средняя к сложностям',
            'typical_rating': '5-7/10'
        },
        'budget_traveler': {
            'name': 'Дмитрий, 28 лет, бюджетный путешественник',
            'priorities': ['Цена', 'Простота', 'Быстрота'],
            'tolerance': 'Высокая к неудобствам',
            'typical_rating': '4-6/10'
        }
    }
    
    for key, persona in personas.items():
        print(f"\n👤 {persona['name']}:")
        print(f"   Приоритеты: {', '.join(persona['priorities'])}")
        print(f"   Толерантность: {persona['tolerance']}")
        print(f"   Типичная оценка: {persona['typical_rating']}")

def calculate_persona_impact():
    """Расчет влияния количества персонажей"""
    
    print(f"\n📊 ВЛИЯНИЕ КОЛИЧЕСТВА ПЕРСОНАЖЕЙ:")
    print("=" * 50)
    
    scenarios = {
        '1_persona': {
            'description': '1 персонаж (быстрый тест)',
            'time': '30 сек',
            'cost': '$0.01',
            'coverage': 'Ограниченная'
        },
        '3_personas': {
            'description': '3 персонажа (баланс)',
            'time': '1-2 мин',
            'cost': '$0.03',
            'coverage': 'Хорошая'
        },
        '5_personas': {
            'description': '5+ персонажей (глубокий анализ)',
            'time': '3-5 мин',
            'cost': '$0.05',
            'coverage': 'Отличная'
        }
    }
    
    for scenario, data in scenarios.items():
        print(f"\n📋 {data['description'].upper()}:")
        print(f"   Время: {data['time']}")
        print(f"   Стоимость: {data['cost']}")
        print(f"   Покрытие: {data['coverage']}")

if __name__ == "__main__":
    user_feedback = analyze_personas()
    explain_persona_differences()
    calculate_persona_impact()
    
    print(f"\n🎉 Анализ персонажей завершен!")
    print(f"💡 {len(user_feedback)} персонажей дают разные перспективы")
    print(f"💡 Каждый персонаж представляет разную аудиторию")
    print(f"💡 Это делает анализ более полным и объективным")


