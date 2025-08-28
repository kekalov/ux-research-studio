"""
Advanced Scenarios - расширенные сценарии с детальными требованиями
"""

def get_advanced_scenarios():
    """Расширенные сценарии с детальными требованиями"""
    
    return {
        'sochi_ski_premium': {
            'name': 'Горнолыжный отдых в Сочи (Премиум)',
            'destination': 'Сочи',
            'check_in': '2024-12-20',
            'check_out': '2024-12-27',
            'guests': 2,
            'rooms': 1,
            'description': 'Забронировать отель в Сочи на зимний горнолыжный период',
            'requirements': {
                'stars': '4+ звезды',
                'distance_to_lift': 'не дальше 2 км от подъемника',
                'cancellation': 'бесплатная отмена бронирования',
                'price_limit': 'до 10 000 рублей за ночь',
                'ski_storage': True,
                'ski_equipment': False,  # Будем брать свое
                'restaurant': True,
                'spa': True,
                'transfer_to_lift': True
            },
            'search_strategy': [
                'Поиск отелей 4-5 звезд в Сочи',
                'Фильтрация по расстоянию до подъемника (до 2 км)',
                'Проверка тарифов с бесплатной отменой',
                'Фильтрация по цене (до 10 000 руб/ночь)',
                'Проверка наличия лыжехранилища',
                'Проверка трансфера к подъемнику'
            ],
            'persona': 'ski_enthusiast'
        },
        
        'andorra_luxury_ski': {
            'name': 'Люксовый горнолыжный отдых в Андорре',
            'destination': 'Андорра',
            'check_in': '2024-12-25',
            'check_out': '2025-01-02',
            'guests': 2,
            'rooms': 1,
            'description': 'Премиум отель в Андорре для горнолыжного отдыха',
            'requirements': {
                'stars': '5 звезд',
                'distance_to_lift': 'ski-in/ski-out или до 500м',
                'cancellation': 'бесплатная отмена',
                'price_limit': 'до 25 000 рублей за ночь',
                'ski_storage': True,
                'ski_equipment': True,
                'restaurant': True,
                'spa': True,
                'pool': True,
                'transfer_to_lift': True
            },
            'search_strategy': [
                'Поиск 5-звездочных отелей в Андорре',
                'Фильтрация по ski-in/ski-out',
                'Проверка включенного оборудования',
                'Фильтрация по цене (до 25 000 руб/ночь)',
                'Проверка спа и бассейна'
            ],
            'persona': 'luxury_ski_traveler'
        },
        
        'budget_ski_sochi': {
            'name': 'Бюджетный горнолыжный отдых в Сочи',
            'destination': 'Сочи',
            'check_in': '2025-01-15',
            'check_out': '2025-01-22',
            'guests': 2,
            'rooms': 1,
            'description': 'Экономичный отель для горнолыжного отдыха',
            'requirements': {
                'stars': '3+ звезды',
                'distance_to_lift': 'до 5 км от подъемника',
                'cancellation': 'гибкая отмена',
                'price_limit': 'до 5 000 рублей за ночь',
                'ski_storage': True,
                'ski_equipment': False,
                'restaurant': False,
                'spa': False,
                'transfer_to_lift': False
            },
            'search_strategy': [
                'Поиск отелей 3-4 звезды в Сочи',
                'Фильтрация по цене (до 5 000 руб/ночь)',
                'Проверка общественного транспорта',
                'Поиск ближайших кафе и ресторанов'
            ],
            'persona': 'budget_ski_traveler'
        }
    }

def get_ski_personas():
    """Персонажи для горнолыжного отдыха"""
    
    return {
        'ski_enthusiast': {
            'name': 'Михаил, 32 года - горнолыжник-энтузиаст',
            'goals': [
                'найти отель рядом с подъемником',
                'получить качественное обслуживание',
                'иметь удобное лыжехранилище',
                'найти тариф с бесплатной отменой'
            ],
            'pain_points': [
                'далекое расстояние до склонов',
                'отсутствие лыжехранилища',
                'жесткие условия отмены',
                'высокие цены'
            ],
            'priorities': ['Удобство', 'Качество', 'Гибкость'],
            'tolerance': 'Средняя',
            'typical_rating': '6-8/10'
        },
        
        'luxury_ski_traveler': {
            'name': 'Елена, 38 лет - люксовый горнолыжник',
            'goals': [
                'ski-in/ski-out отель',
                'включенное оборудование',
                'спа и бассейн',
                'высокий уровень сервиса'
            ],
            'pain_points': [
                'отсутствие ski-in/ski-out',
                'дополнительные платежи',
                'плохой сервис',
                'отсутствие спа'
            ],
            'priorities': ['Комфорт', 'Сервис', 'Качество'],
            'tolerance': 'Низкая',
            'typical_rating': '7-9/10'
        },
        
        'budget_ski_traveler': {
            'name': 'Антон, 25 лет - бюджетный горнолыжник',
            'goals': [
                'дешевый отель',
                'близко к склонам',
                'базовая инфраструктура',
                'экономия на всем'
            ],
            'pain_points': [
                'высокие цены',
                'далекое расположение',
                'отсутствие транспорта',
                'скрытые доплаты'
            ],
            'priorities': ['Цена', 'Расстояние', 'Простота'],
            'tolerance': 'Высокая',
            'typical_rating': '4-6/10'
        }
    }

def get_enhanced_search_prompt(scenario_name):
    """Расширенный промпт для поиска"""
    
    scenarios = get_advanced_scenarios()
    scenario = scenarios.get(scenario_name, {})
    
    if not scenario:
        return "Базовый поиск отеля"
    
    requirements = scenario.get('requirements', {})
    strategy = scenario.get('search_strategy', [])
    
    prompt = f"""
🎿 РАСШИРЕННЫЙ ПОИСК: {scenario['name']}

📍 Направление: {scenario['destination']}
📅 Даты: {scenario['check_in']} - {scenario['check_out']}
👥 Гости: {scenario['guests']} человека, {scenario['rooms']} комната

🎯 ТРЕБОВАНИЯ:
• Звезды: {requirements.get('stars', 'Любые')}
• Расстояние до подъемника: {requirements.get('distance_to_lift', 'Любое')}
• Отмена: {requirements.get('cancellation', 'Любая')}
• Цена: {requirements.get('price_limit', 'Любая')}
• Лыжехранилище: {'Да' if requirements.get('ski_storage') else 'Нет'}
• Трансфер к подъемнику: {'Да' if requirements.get('transfer_to_lift') else 'Нет'}

🔍 СТРАТЕГИЯ ПОИСКА:
"""
    
    for i, step in enumerate(strategy, 1):
        prompt += f"{i}. {step}\n"
    
    prompt += f"""
💡 ДОПОЛНИТЕЛЬНЫЕ ПРОВЕРКИ:
• Наличие отзывов о горнолыжном сервисе
• Качество лыжехранилища
• Расстояние до ближайшего подъемника
• Наличие трансфера
• Условия отмены бронирования
• Включенные услуги

🎯 ЦЕЛЬ: Найти идеальный отель для горнолыжного отдыха согласно всем требованиям.
"""
    
    return prompt


