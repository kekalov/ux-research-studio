"""
Show Ski Report Summary - показ краткой сводки отчета
"""

import json
from pathlib import Path

def show_ski_report_summary():
    """Показать краткую сводку отчета по горнолыжному исследованию"""
    
    # Находим последний отчет
    reports_dir = Path('reports')
    ski_reports = list(reports_dir.glob('ski_research_report_*.json'))
    
    if not ski_reports:
        print("❌ Отчеты по горнолыжному исследованию не найдены")
        return
    
    # Берем самый свежий отчет
    latest_report = max(ski_reports, key=lambda x: x.stat().st_mtime)
    
    print("🎿 ОТЧЕТ ПО ГОРНОЛЫЖНОМУ ИССЛЕДОВАНИЮ")
    print("=" * 60)
    print(f"📁 Файл: {latest_report.name}")
    
    # Читаем отчет
    with open(latest_report, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Основная информация
    scenario = data.get('scenario', 'Неизвестно')
    config = data.get('config', {})
    steps = data.get('steps', [])
    analysis = data.get('analysis', {})
    user_feedback = data.get('user_feedback', {})
    
    print(f"\n📋 ОСНОВНАЯ ИНФОРМАЦИЯ:")
    print(f"   Сценарий: {scenario}")
    print(f"   Направление: {config.get('destination', 'Неизвестно')}")
    print(f"   Даты: {config.get('check_in', '')} - {config.get('check_out', '')}")
    print(f"   Гости: {config.get('guests', 0)} человека")
    
    # Требования
    requirements = config.get('requirements', {})
    print(f"\n🎯 ТРЕБОВАНИЯ:")
    print(f"   Звезды: {requirements.get('stars', 'Любые')}")
    print(f"   Расстояние до подъемника: {requirements.get('distance_to_lift', 'Любое')}")
    print(f"   Отмена: {requirements.get('cancellation', 'Любая')}")
    print(f"   Цена: {requirements.get('price_limit', 'Любая')}")
    print(f"   Лыжехранилище: {'Да' if requirements.get('ski_storage') else 'Нет'}")
    print(f"   Трансфер: {'Да' if requirements.get('transfer_to_lift') else 'Нет'}")
    
    # Статистика
    successful_steps = [s for s in steps if s.get('success', False)]
    total_time = sum(s.get('duration', 0) for s in steps)
    
    print(f"\n📊 СТАТИСТИКА:")
    print(f"   Всего шагов: {len(steps)}")
    print(f"   Успешных шагов: {len(successful_steps)}")
    print(f"   Успешность: {len(successful_steps)/len(steps)*100:.1f}%")
    print(f"   Общее время: {total_time:.1f} сек")
    
    # AI анализ
    print(f"\n🤖 AI АНАЛИЗ:")
    print(f"   Общая оценка: {analysis.get('overall_score', 'N/A')}/10")
    print(f"   Время выполнения: {analysis.get('total_time', 0):.1f} сек")
    print(f"   Успешность: {analysis.get('success_rate', 0):.1f}%")
    
    # Метрики удобства
    usability = analysis.get('usability_metrics', {})
    if usability:
        print(f"\n📈 МЕТРИКИ УДОБСТВА:")
        print(f"   Простота использования: {usability.get('ease_of_use', 'N/A')}/10")
        print(f"   Эффективность: {usability.get('efficiency', 'N/A')}/10")
        print(f"   Удовлетворенность: {usability.get('satisfaction', 'N/A')}/10")
        print(f"   Обучаемость: {usability.get('learnability', 'N/A')}/10")
    
    # Ключевые находки
    key_findings = analysis.get('key_findings', [])
    if key_findings:
        print(f"\n✅ КЛЮЧЕВЫЕ НАХОДКИ:")
        for finding in key_findings:
            print(f"   • {finding}")
    
    # Выявленные проблемы
    issues = analysis.get('issues_identified', [])
    if issues:
        print(f"\n⚠️  ВЫЯВЛЕННЫЕ ПРОБЛЕМЫ:")
        for issue in issues:
            print(f"   • {issue}")
    
    # Рекомендации
    recommendations = analysis.get('recommendations', [])
    if recommendations:
        print(f"\n💡 РЕКОМЕНДАЦИИ:")
        for rec in recommendations:
            priority_emoji = "🔴" if rec.get('priority') == 'high' else "🟡" if rec.get('priority') == 'medium' else "🟢"
            print(f"   {priority_emoji} {rec.get('description', '')}")
            print(f"      Влияние: {rec.get('impact', '')}")
    
    # Анализ результатов поиска
    for step in steps:
        if step.get('action') == 'analyze_ski_results':
            analysis_data = step.get('analysis', {})
            print(f"\n🏨 АНАЛИЗ РЕЗУЛЬТАТОВ ПОИСКА:")
            print(f"   Найдено отелей: {analysis_data.get('hotels_count', 0)}")
            
            ski_facilities = analysis_data.get('ski_facilities', {})
            print(f"   С лыжехранилищем: {ski_facilities.get('with_ski_storage', 0)}")
            print(f"   С трансфером: {ski_facilities.get('with_transfer', 0)}")
            print(f"   Ski-in/ski-out: {ski_facilities.get('ski_in_ski_out', 0)}")
            print(f"   С оборудованием: {ski_facilities.get('with_equipment', 0)}")
            
            distance = analysis_data.get('distance_analysis', {})
            print(f"   В пределах 1 км: {distance.get('within_1km', 0)}")
            print(f"   В пределах 2 км: {distance.get('within_2km', 0)}")
            print(f"   В пределах 5 км: {distance.get('within_5km', 0)}")
            
            cancellation = analysis_data.get('cancellation_policies', {})
            print(f"   С бесплатной отменой: {cancellation.get('free_cancellation', 0)}")
            print(f"   С гибкой отменой: {cancellation.get('flexible', 0)}")
            print(f"   С жесткой отменой: {cancellation.get('strict', 0)}")
            break
    
    # Фидбэк от персонажей
    print(f"\n👥 ФИДБЭК ОТ ПЕРСОНАЖЕЙ:")
    for persona_key, feedback in user_feedback.items():
        persona = feedback.get('user_persona', {})
        rating = feedback.get('usability_score', {}).get('score', 0)
        print(f"   👤 {persona.get('name', persona_key)}: {rating}/10")
    
    # Ключевые шаги
    print(f"\n🔍 КЛЮЧЕВЫЕ ШАГИ:")
    for step in steps:
        if any(keyword in step.get('action', '') for keyword in ['ski', 'lift', 'cancellation', 'price', 'star']):
            status = "✅" if step.get('success') else "❌"
            print(f"   {status} {step.get('description', '')}")
    
    print(f"\n📁 ПОЛНЫЙ ОТЧЕТ:")
    print(f"   HTML: reports/ux_report_{scenario}_*.html")
    print(f"   JSON: {latest_report.name}")
    print(f"   Графики: reports/*_{scenario}_*.png")
    
    print(f"\n🎉 СВОДКА ЗАВЕРШЕНА!")

if __name__ == "__main__":
    show_ski_report_summary()


