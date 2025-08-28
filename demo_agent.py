#!/usr/bin/env python3
"""
Демонстрационная версия AI UX Research Agent без браузера
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime

# Добавление корневой папки в путь
sys.path.append(str(Path(__file__).parent))

from config.settings import load_config
from agent.ai_analyzer import AIAnalyzer
from reports.report_generator import ReportGenerator

def demo_agent():
    """Демонстрация работы AI агента без браузера"""
    
    print("🎭 Демонстрация AI UX Research Agent")
    print("=" * 50)
    
    # Загрузка конфигурации
    config = load_config()
    
    print("📋 Конфигурация загружена:")
    print(f"   - Базовый URL: {config['base_url']}")
    print(f"   - Доступные сценарии: {list(config['scenarios'].keys())}")
    
    # Проверка OpenAI API
    if os.getenv('OPENAI_API_KEY'):
        print("✅ OpenAI API ключ найден")
    else:
        print("⚠️  OpenAI API ключ не найден (будет использован базовый анализ)")
    
    print("\n🚀 Создание демонстрационных данных...")
    
    # Создание демонстрационных результатов
    demo_results = create_demo_results(config)
    
    print("✅ Демонстрационные данные созданы")
    
    # Инициализация AI анализатора
    ai_analyzer = AIAnalyzer(config['ai'])
    
    print("\n🤖 Выполнение AI анализа...")
    
    # AI анализ результатов
    ai_analysis = ai_analyzer.analyze_results(demo_results)
    
    print("✅ AI анализ завершен")
    
    # Добавление AI анализа к результатам
    demo_results['analysis'] = ai_analysis
    
    # Генерация отчета
    print("\n📊 Генерация отчета...")
    
    report_generator = ReportGenerator()
    report_path = report_generator.generate_report(demo_results, 'demo_scenario', 'reports')
    
    print(f"✅ Отчет сохранен: {report_path}")
    
    # Вывод краткой сводки
    print("\n📈 Краткая сводка результатов:")
    print(f"   - Сценарий: {demo_results['scenario']}")
    print(f"   - Всего шагов: {len(demo_results['steps'])}")
    print(f"   - Успешных шагов: {len([s for s in demo_results['steps'] if s.get('success', False)])}")
    print(f"   - Общий балл: {ai_analysis.get('overall_score', 'N/A')}/10")
    print(f"   - Резюме: {ai_analysis.get('summary', 'N/A')}")
    
    # Вывод рекомендаций
    recommendations = ai_analysis.get('recommendations', [])
    if recommendations:
        print(f"\n🔧 Топ-3 рекомендации:")
        for i, rec in enumerate(recommendations[:3], 1):
            print(f"   {i}. {rec.get('description', 'N/A')}")
    
    print("\n🎉 Демонстрация завершена!")
    print(f"📁 Полный отчет доступен в: {report_path}")

def create_demo_results(config):
    """Создание демонстрационных результатов"""
    
    # Демонстрационные шаги
    demo_steps = [
        {
            'action': 'search_destination',
            'destination': 'Сочи',
            'success': True,
            'timestamp': datetime.now().timestamp() - 30,
            'duration': 2.5
        },
        {
            'action': 'select_dates',
            'check_in': '2024-12-20',
            'check_out': '2024-12-27',
            'success': True,
            'timestamp': datetime.now().timestamp() - 25,
            'duration': 3.2
        },
        {
            'action': 'configure_guests',
            'guests': 2,
            'rooms': 1,
            'success': True,
            'timestamp': datetime.now().timestamp() - 20,
            'duration': 1.8
        },
        {
            'action': 'search_hotels',
            'success': True,
            'timestamp': datetime.now().timestamp() - 15,
            'duration': 4.5
        },
        {
            'action': 'analyze_search_results',
            'analysis': {
                'hotels_count': 45,
                'filters_available': ['Цена', 'Звезды', 'Удобства', 'Район'],
                'sorting_options': ['По цене', 'По рейтингу', 'По популярности'],
                'hotel_cards': {
                    'total_cards': 45,
                    'cards_with_images': 42,
                    'cards_with_prices': 45,
                    'cards_with_ratings': 38,
                    'average_price': 8500
                },
                'pagination': {
                    'has_pagination': True,
                    'current_page': 1,
                    'total_pages': 3,
                    'next_page_available': True
                },
                'price_range': {
                    'min_price': 3500,
                    'max_price': 25000,
                    'price_distribution': {
                        '3500-7000': 15,
                        '7000-10500': 20,
                        '10500-14000': 8,
                        '14000-17500': 2
                    }
                }
            },
            'success': True,
            'timestamp': datetime.now().timestamp() - 10,
            'duration': 2.1
        },
        {
            'action': 'apply_price_filter',
            'success': True,
            'timestamp': datetime.now().timestamp() - 8,
            'duration': 1.5
        },
        {
            'action': 'apply_star_filter',
            'success': False,
            'error': 'Элемент фильтра не найден',
            'timestamp': datetime.now().timestamp() - 6,
            'duration': 5.2
        }
    ]
    
    # Создание результатов
    results = {
        'scenario': 'sochi_winter',
        'timestamp': datetime.now().timestamp(),
        'config': config['scenarios']['sochi_winter'],
        'steps': demo_steps,
        'analysis': {},
        'screenshots': []
    }
    
    return results

if __name__ == "__main__":
    demo_agent()


