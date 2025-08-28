#!/usr/bin/env python3
"""
Пример использования AI UX Research Agent для Ostrovok.ru
"""

import os
import sys
from pathlib import Path

# Добавление корневой папки в путь
sys.path.append(str(Path(__file__).parent.parent))

from agent.ux_agent import UXResearchAgent
from config.settings import load_config

def main():
    """Пример использования AI агента"""
    
    print("🚀 AI UX Research Agent для Ostrovok.ru")
    print("=" * 50)
    
    # Загрузка конфигурации
    config = load_config()
    
    # Проверка наличия OpenAI API ключа
    if not os.getenv('OPENAI_API_KEY'):
        print("⚠️  ВНИМАНИЕ: OPENAI_API_KEY не установлен в переменных окружения")
        print("   AI анализ будет ограничен базовыми возможностями")
        print("   Для полного функционала установите переменную окружения:")
        print("   export OPENAI_API_KEY='your-api-key-here'")
        print()
    
    # Создание и запуск агента
    with UXResearchAgent(config, headless=False) as agent:
        
        print("📋 Доступные сценарии:")
        print("1. sochi_winter - Поиск отелей в Сочи на зимний сезон")
        print("2. andorra - Поиск отелей в Андорре")
        print("3. full_analysis - Полный анализ всех функций")
        print()
        
        # Выполнение сценария Сочи
        print("🏨 Выполнение сценария: Поиск отелей в Сочи")
        print("-" * 40)
        
        try:
            results = agent.run_scenario('sochi_winter')
            
            print(f"✅ Сценарий выполнен успешно!")
            print(f"📊 Результаты:")
            print(f"   - Всего шагов: {len(results.get('steps', []))}")
            print(f"   - Успешных шагов: {len([s for s in results.get('steps', []) if s.get('success', False)])}")
            
            # Вывод деталей каждого шага
            for i, step in enumerate(results.get('steps', []), 1):
                status = "✅" if step.get('success', False) else "❌"
                print(f"   {i}. {status} {step.get('action', 'Unknown')} ({step.get('duration', 0):.2f}с)")
                if step.get('error'):
                    print(f"      Ошибка: {step['error']}")
            
            # Вывод AI анализа
            ai_analysis = results.get('analysis', {})
            if ai_analysis:
                print(f"\n🤖 AI Анализ:")
                print(f"   - Общий балл: {ai_analysis.get('overall_score', 'N/A')}/10")
                print(f"   - Резюме: {ai_analysis.get('summary', 'N/A')}")
                
                # Вывод рекомендаций
                recommendations = ai_analysis.get('recommendations', [])
                if recommendations:
                    print(f"   - Рекомендации:")
                    for rec in recommendations[:3]:  # Показываем первые 3
                        print(f"     • {rec.get('description', 'N/A')}")
            
        except Exception as e:
            print(f"❌ Ошибка при выполнении сценария: {e}")
        
        print("\n" + "=" * 50)
        
        # Выполнение сценария Андорры
        print("🏔️ Выполнение сценария: Поиск отелей в Андорре")
        print("-" * 40)
        
        try:
            results = agent.run_scenario('andorra')
            
            print(f"✅ Сценарий выполнен успешно!")
            print(f"📊 Результаты:")
            print(f"   - Всего шагов: {len(results.get('steps', []))}")
            print(f"   - Успешных шагов: {len([s for s in results.get('steps', []) if s.get('success', False)])}")
            
        except Exception as e:
            print(f"❌ Ошибка при выполнении сценария: {e}")
    
    print("\n🎉 Исследование завершено!")
    print("📁 Отчеты сохранены в папке 'reports/'")

if __name__ == "__main__":
    main()


