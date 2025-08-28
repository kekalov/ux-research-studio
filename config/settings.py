"""
Конфигурация для AI UX Research Agent
"""

import os
from pathlib import Path
from typing import Dict, Any

def load_config() -> Dict[str, Any]:
    """Загрузка конфигурации"""
    
    config = {
        # Основные настройки
        'base_url': 'https://ostrovok.ru',
        'user_agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
        
        # Настройки браузера
        'browser': {
            'implicit_wait': 10,
            'page_load_timeout': 30,
            'window_size': (1920, 1080)
        },
        
        # Настройки AI
        'ai': {
            'model': 'gpt-4',
            'temperature': 0.7,
            'max_tokens': 2000
        },
        
        # Сценарии исследования
        'scenarios': {
            'sochi_winter': {
                'destination': 'Сочи',
                'check_in': '2024-12-20',
                'check_out': '2024-12-27',
                'guests': 2,
                'rooms': 1,
                'description': 'Поиск отелей в Сочи на зимний сезон'
            },
            'andorra': {
                'destination': 'Андорра',
                'check_in': '2024-12-25',
                'check_out': '2025-01-02',
                'guests': 2,
                'rooms': 1,
                'description': 'Поиск отелей в Андорре для горнолыжного отдыха'
            },
            'full_analysis': {
                'description': 'Полный анализ всех функций сайта'
            }
        },
        
        # Элементы для анализа
        'selectors': {
            'search_box': 'input[name="query"]',
            'date_picker': '.date-picker',
            'guests_selector': '.guests-selector',
            'search_button': 'button[type="submit"]',
            'hotel_cards': '.hotel-card',
            'filters': '.filters',
            'sort_options': '.sort-options',
            'booking_button': '.booking-button'
        },
        
        # Временные задержки
        'delays': {
            'page_load': 3,
            'element_wait': 2,
            'user_action': 1
        }
    }
    
    return config

def get_env_config() -> Dict[str, str]:
    """Получение конфигурации из переменных окружения"""
    
    env_config = {}
    
    # OpenAI API ключ
    openai_key = os.getenv('OPENAI_API_KEY')
    if openai_key:
        env_config['openai_api_key'] = openai_key
    
    # Прокси настройки (опционально)
    proxy = os.getenv('HTTP_PROXY')
    if proxy:
        env_config['proxy'] = proxy
    
    return env_config


