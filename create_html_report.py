"""
HTML Report Generator - создание HTML отчета из JSON данных
"""

import json
import os
from datetime import datetime
from pathlib import Path

def create_html_report(json_file_path: str) -> str:
    """Создание HTML отчета из JSON файла"""
    
    # Читаем JSON данные
    with open(json_file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Извлекаем данные
    scenario = data.get('scenario', 'unknown')
    steps = data.get('steps', [])
    analysis = data.get('analysis', {})
    user_feedback = data.get('user_feedback', {})
    
    # Подсчитываем статистику
    total_steps = len(steps)
    successful_steps = len([s for s in steps if s.get('success', False)])
    failed_steps = total_steps - successful_steps
    total_time = sum(s.get('duration', 0) for s in steps)
    
    # Создаем HTML
    html_content = f"""
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>UX Research Report - {scenario}</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        .header {{
            text-align: center;
            border-bottom: 3px solid #007bff;
            padding-bottom: 20px;
            margin-bottom: 30px;
        }}
        .header h1 {{
            color: #007bff;
            margin: 0;
        }}
        .summary-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        .summary-card {{
            background: #f8f9fa;
            padding: 20px;
            border-radius: 8px;
            text-align: center;
            border-left: 4px solid #007bff;
        }}
        .summary-card h3 {{
            margin: 0 0 10px 0;
            color: #007bff;
        }}
        .summary-card .value {{
            font-size: 2em;
            font-weight: bold;
            color: #333;
        }}
        .section {{
            margin-bottom: 30px;
        }}
        .section h2 {{
            color: #333;
            border-bottom: 2px solid #007bff;
            padding-bottom: 10px;
        }}
        .step-table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 15px;
        }}
        .step-table th, .step-table td {{
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }}
        .step-table th {{
            background-color: #007bff;
            color: white;
        }}
        .step-table tr:nth-child(even) {{
            background-color: #f2f2f2;
        }}
        .success {{
            color: #28a745;
            font-weight: bold;
        }}
        .error {{
            color: #dc3545;
            font-weight: bold;
        }}
        .user-feedback {{
            background: #fff3cd;
            border: 1px solid #ffeaa7;
            border-radius: 5px;
            padding: 15px;
            margin-bottom: 10px;
        }}
        .persona-card {{
            background: #e3f2fd;
            border: 1px solid #bbdefb;
            border-radius: 8px;
            padding: 20px;
            margin-bottom: 15px;
        }}
        .persona-name {{
            font-weight: bold;
            color: #1976d2;
            margin-bottom: 10px;
        }}
        .emotional-journey {{
            display: flex;
            overflow-x: auto;
            gap: 10px;
            padding: 15px 0;
        }}
        .emotion-step {{
            min-width: 120px;
            padding: 10px;
            border-radius: 5px;
            text-align: center;
            font-size: 0.9em;
        }}
        .emotion-neutral {{ background: #e9ecef; }}
        .emotion-curious {{ background: #fff3cd; }}
        .emotion-satisfied {{ background: #d4edda; }}
        .emotion-focused {{ background: #cce5ff; }}
        .emotion-frustrated {{ background: #f8d7da; }}
        .emotion-excited {{ background: #d1ecf1; }}
        .emotion-pleased {{ background: #d4edda; }}
        .emotion-interested {{ background: #fff3cd; }}
        .emotion-concentrated {{ background: #cce5ff; }}
        .emotion-confident {{ background: #d4edda; }}
        .emotion-patient {{ background: #e2e3e5; }}
        .emotion-exploring {{ background: #fff3cd; }}
        .emotion-engaged {{ background: #d1ecf1; }}
        .emotion-hopeful {{ background: #d4edda; }}
        .emotion-deciding {{ background: #cce5ff; }}
        .emotion-determined {{ background: #fff3cd; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎭 UX Research Report</h1>
            <p>AI Agent Simulation - {scenario.replace('_', ' ').title()}</p>
            <p>Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        </div>

        <div class="summary-grid">
            <div class="summary-card">
                <h3>Общий балл</h3>
                <div class="value">{analysis.get('overall_score', 'N/A')}/10</div>
            </div>
            <div class="summary-card">
                <h3>Успешность</h3>
                <div class="value">{successful_steps}/{total_steps}</div>
            </div>
            <div class="summary-card">
                <h3>Общее время</h3>
                <div class="value">{total_time:.1f} сек</div>
            </div>
            <div class="summary-card">
                <h3>Оценка опыта</h3>
                <div class="value">{analysis.get('experience_rating', 'N/A')}</div>
            </div>
        </div>

        <div class="section">
            <h2>📋 Детализация шагов</h2>
            <table class="step-table">
                <thead>
                    <tr>
                        <th>Шаг</th>
                        <th>Действие</th>
                        <th>Длительность</th>
                        <th>Статус</th>
                        <th>Мысли пользователя</th>
                        <th>Эмоциональное состояние</th>
                    </tr>
                </thead>
                <tbody>
    """
    
    # Добавляем строки таблицы для каждого шага
    for step in steps:
        status_class = "success" if step.get('success', False) else "error"
        status_text = "✅ Успешно" if step.get('success', False) else "❌ Ошибка"
        duration = step.get('duration', 0)
        user_thoughts = step.get('user_thoughts', '')
        emotional_state = step.get('emotional_state', 'neutral')
        
        html_content += f"""
                    <tr>
                        <td>{step.get('step_number', '')}</td>
                        <td>{step.get('description', '')}</td>
                        <td>{duration:.1f} сек</td>
                        <td class="{status_class}">{status_text}</td>
                        <td>"{user_thoughts}"</td>
                        <td>{emotional_state}</td>
                    </tr>
        """
    
    html_content += """
                </tbody>
            </table>
        </div>

        <div class="section">
            <h2>👥 Фидбэк от пользователей</h2>
    """
    
    # Добавляем фидбэк от каждого персонажа
    for persona_key, feedback in user_feedback.items():
        persona = feedback.get('persona', {})
        rating = feedback.get('rating', 0)
        impression = feedback.get('impression', '')
        
        html_content += f"""
            <div class="persona-card">
                <div class="persona-name">👤 {persona.get('name', 'Unknown')}</div>
                <p><strong>Оценка:</strong> {rating}/10</p>
                <p><strong>Впечатление:</strong> {impression}</p>
                <p><strong>Цели:</strong> {', '.join(persona.get('goals', []))}</p>
                <p><strong>Болевые точки:</strong> {', '.join(persona.get('pain_points', []))}</p>
            </div>
        """
    
    html_content += """
        </div>

        <div class="section">
            <h2>🎭 Эмоциональный путь пользователя</h2>
            <div class="emotional-journey">
    """
    
    # Добавляем эмоциональный путь
    for step in steps:
        emotional_state = step.get('emotional_state', 'neutral')
        step_number = step.get('step_number', '')
        duration = step.get('duration', 0)
        
        html_content += f"""
                <div class="emotion-step emotion-{emotional_state}">
                    <div><strong>Шаг {step_number}</strong></div>
                    <div>{emotional_state}</div>
                    <div>{duration:.1f}с</div>
                </div>
        """
    
    html_content += """
            </div>
        </div>

        <div class="section">
            <h2>🔍 Выявленные проблемы</h2>
            <ul>
    """
    
    # Добавляем проблемы
    issues = analysis.get('issues_identified', [])
    for issue in issues:
        html_content += f"<li>{issue}</li>"
    
    html_content += """
            </ul>
        </div>

        <div class="section">
            <h2>💡 Рекомендации</h2>
    """
    
    # Добавляем рекомендации
    recommendations = analysis.get('recommendations', [])
    for rec in recommendations:
        priority_color = '#dc3545' if rec.get('priority') == 'high' else '#ffc107' if rec.get('priority') == 'medium' else '#28a745'
        html_content += f"""
            <div class="user-feedback" style="border-left: 4px solid {priority_color};">
                <strong>Приоритет: {rec.get('priority', 'low')}</strong><br>
                {rec.get('description', '')}<br>
                <em>Влияние: {rec.get('impact', '')}</em>
            </div>
        """
    
    html_content += """
        </div>

        <div class="section">
            <h2>📊 Анализ результатов поиска</h2>
    """
    
    # Добавляем анализ результатов поиска
    for step in steps:
        if step.get('action') == 'analyze_results' and step.get('analysis'):
            analysis_data = step.get('analysis', {})
            html_content += f"""
                <div class="summary-grid">
                    <div class="summary-card">
                        <h3>Найдено отелей</h3>
                        <div class="value">{analysis_data.get('hotels_count', 0)}</div>
                    </div>
                    <div class="summary-card">
                        <h3>Средняя цена</h3>
                        <div class="value">{analysis_data.get('hotel_cards', {}).get('average_price', 0)} ₽</div>
                    </div>
                    <div class="summary-card">
                        <h3>Доступные фильтры</h3>
                        <div class="value">{len(analysis_data.get('filters_available', []))}</div>
                    </div>
                    <div class="summary-card">
                        <h3>Страниц результатов</h3>
                        <div class="value">{analysis_data.get('pagination', {}).get('total_pages', 0)}</div>
                    </div>
                </div>
            """
            break
    
    html_content += """
        </div>
    </div>
</body>
</html>
    """
    
    # Сохраняем HTML файл
    output_path = json_file_path.replace('.json', '_report.html')
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    return output_path

if __name__ == "__main__":
    # Находим последний JSON файл
    reports_dir = Path('reports')
    json_files = list(reports_dir.glob('simple_ux_report_*.json'))
    
    if json_files:
        latest_file = max(json_files, key=lambda x: x.stat().st_mtime)
        print(f"Создание HTML отчета для: {latest_file}")
        
        html_path = create_html_report(str(latest_file))
        print(f"✅ HTML отчет создан: {html_path}")
        
        # Открываем в браузере
        import subprocess
        subprocess.run(['open', html_path])
    else:
        print("❌ JSON файлы не найдены в папке reports/")


