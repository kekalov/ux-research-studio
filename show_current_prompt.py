"""
Show Current Prompt - показать текущий промпт для поиска
"""

from config.advanced_scenarios import get_enhanced_search_prompt, get_advanced_scenarios

def show_current_prompt():
    """Показать текущий промпт для поиска"""
    
    print("🎿 ТЕКУЩИЙ ПРОМПТ ДЛЯ ПОИСКА")
    print("=" * 60)
    
    # Показываем доступные сценарии
    scenarios = get_advanced_scenarios()
    print(f"\n📋 ДОСТУПНЫЕ СЦЕНАРИИ:")
    for key, scenario in scenarios.items():
        print(f"   • {key}: {scenario['name']}")
    
    # Показываем промпт для основного сценария
    scenario_name = 'sochi_ski_premium'
    print(f"\n🎯 ПРОМПТ ДЛЯ СЦЕНАРИЯ: {scenario_name}")
    print("=" * 60)
    
    prompt = get_enhanced_search_prompt(scenario_name)
    print(prompt)
    
    print("\n" + "=" * 60)
    print("📋 КОПИРУЙТЕ ЭТОТ ПРОМПТ В ОТЧЕТ")
    print("=" * 60)

if __name__ == "__main__":
    show_current_prompt()


