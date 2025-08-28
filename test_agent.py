#!/usr/bin/env python3
"""
Тестовый скрипт для демонстрации работы AI UX Research Agent
"""

import os
import sys
from pathlib import Path

# Добавление корневой папки в путь
sys.path.append(str(Path(__file__).parent))

from agent.ux_agent import UXResearchAgent
from config.settings import load_config

def test_agent():
    """Тестирование AI агента"""
    
    print("🧪 Тестирование AI UX Research Agent")
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
    
    print("\n🚀 Запуск тестового сценария...")
    
    try:
        # Создание агента в headless режиме для быстрого теста
        with UXResearchAgent(config, headless=True) as agent:
            
            print("✅ Агент инициализирован успешно")
            
            # Тестирование базовой функциональности
            print("\n📊 Тестирование анализа главной страницы...")
            
            # Переход на главную страницу
            agent.navigate_to_homepage()
            print("✅ Переход на главную страницу выполнен")
            
            # Анализ главной страницы
            homepage_analysis = agent.analyze_homepage()
            print(f"✅ Анализ главной страницы завершен")
            
            if homepage_analysis.get('success'):
                analysis_data = homepage_analysis.get('analysis', {})
                print(f"   - Заголовок страницы: {analysis_data.get('page_title', 'N/A')}")
                print(f"   - Найдено изображений: {analysis_data.get('performance_indicators', {}).get('images_count', 0)}")
                print(f"   - Найдено скриптов: {analysis_data.get('performance_indicators', {}).get('scripts_count', 0)}")
            else:
                print(f"❌ Ошибка анализа: {homepage_analysis.get('error', 'Unknown error')}")
            
            print("\n🎉 Тестирование завершено успешно!")
            
    except Exception as e:
        print(f"❌ Ошибка при тестировании: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_agent()


