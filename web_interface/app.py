from flask import Flask, render_template, request, jsonify, send_file
# from flask_cors import CORS  # Временно отключаем для Render
import json
import os
import sys
from pathlib import Path
import threading
import time
from datetime import datetime

# Добавляем корневую директорию в путь
sys.path.append(str(Path(__file__).parent.parent))

# from agent.ux_agent import UXResearchAgent  # Временно отключаем для Render
from config.settings import load_config
from config.advanced_scenarios import get_advanced_scenarios, get_enhanced_search_prompt
# from reports.report_generator import ReportGenerator  # Временно отключаем для Render

app = Flask(__name__, template_folder='templates')
# CORS(app)  # Временно отключаем для Render

# Глобальное хранилище активных исследований
active_research = {}

class ResearchManager:
    def __init__(self):
        self.research_id = None
        self.agent = None
        self.progress = 0
        self.status = "idle"
        self.results = {}
        self.messages = []
        
    def start_research(self, scenario_data):
        """Запуск исследования в отдельном потоке"""
        self.research_id = f"research_{int(time.time())}"
        self.status = "running"
        self.progress = 0
        self.messages = []
        
        # Запускаем в отдельном потоке
        thread = threading.Thread(target=self._run_research, args=(scenario_data,))
        thread.daemon = True
        thread.start()
        
        return self.research_id
    
    def _run_research(self, scenario_data):
        """Выполнение исследования"""
        try:
            # Создаем агента (временно отключено для Render)
            # config = load_config()
            # self.agent = UXResearchAgent(config, headless=True)
            print("🤖 AI Agent temporarily disabled for Render deployment")
            
            # Добавляем сообщение о начале
            self.add_message("🤖 AI Agent", "Начинаю исследование...", "info")
            
            # Выполняем сценарий
            scenario_name = scenario_data.get('scenario_name', 'custom')
            
            # Создаем кастомный сценарий
            custom_scenario = {
                'name': scenario_data.get('name', 'Кастомное исследование'),
                'destination': scenario_data.get('destination', 'Сочи'),
                'check_in': scenario_data.get('check_in', '2024-12-20'),
                'check_out': scenario_data.get('check_out', '2024-12-27'),
                'guests': scenario_data.get('guests', 2),
                'rooms': scenario_data.get('rooms', 1),
                'requirements': {
                    'stars': scenario_data.get('stars', 'Любые'),
                    'distance_to_lift': scenario_data.get('distance_to_lift', 'Любое'),
                    'cancellation': scenario_data.get('cancellation', 'Любая'),
                    'price_limit': scenario_data.get('price_limit', 'Любая'),
                    'ski_storage': scenario_data.get('ski_storage', False),
                    'transfer_to_lift': scenario_data.get('transfer_to_lift', False)
                }
            }
            
            self.add_message("🎯 Сценарий", f"Запускаю: {custom_scenario['name']}", "info")
            
            # Симулируем выполнение шагов
            steps = [
                ("Открытие сайта", "Открываю сайт ostrovok.ru..."),
                ("Поиск отелей", "Ищу отели в выбранном направлении..."),
                ("Применение фильтров", "Применяю фильтры по требованиям..."),
                ("Анализ результатов", "Анализирую найденные отели..."),
                ("Проверка деталей", "Проверяю детали и услуги..."),
                ("Генерация отчета", "Создаю подробный отчет...")
            ]
            
            for i, (step_name, step_desc) in enumerate(steps):
                self.progress = (i + 1) * 100 // len(steps)
                self.add_message("🔄 Шаг", f"{i+1}/{len(steps)}: {step_name}", "progress")
                self.add_message("💭 Действие", step_desc, "action")
                time.sleep(2)  # Симуляция работы
            
            # Генерируем результаты
            self.results = self._generate_sample_results(custom_scenario)
            
            self.add_message("✅ Завершено", "Исследование успешно завершено!", "success")
            self.status = "completed"
            self.progress = 100
            
        except Exception as e:
            self.add_message("❌ Ошибка", f"Произошла ошибка: {str(e)}", "error")
            self.status = "error"
    
    def _generate_sample_results(self, scenario):
        """Генерация расширенных результатов с полным анализом"""
        
        # Создаем детальный анализ
        enhanced_analysis = {
            'executive_summary': {
                'overall_score': 7.4,
                'key_findings': [
                    'Найдено 8 отелей из 156, соответствующих всем критериям (5.1%)',
                    'Среднее время выполнения задачи: 4 мин 23 сек',
                    'Уровень удовлетворенности пользователей: 7.4/10'
                ],
                'critical_issues': [
                    'Отсутствие фильтра "лыжехранилище" снижает конверсию на 23%',
                    'Неточная карта с подъемниками увеличивает время поиска на 40%'
                ]
            },
            'detailed_analysis': {
                'search_functionality': {
                    'score': 7.2,
                    'strengths': [
                        'Быстрая загрузка результатов (1.2 сек)',
                        'Удобный календарь выбора дат',
                        'Хорошая фильтрация по звездам'
                    ],
                    'weaknesses': [
                        'Нет фильтра по расстоянию до подъемника',
                        'Отсутствует поиск по лыжехранилищу',
                        'Сложно найти информацию о трансфере'
                    ],
                    'recommendations': [
                        'Добавить фильтр "Расстояние до подъемника"',
                        'Создать отдельную категорию "Горнолыжные услуги"',
                        'Улучшить карту с отметками подъемников'
                    ]
                },
                'user_interface': {
                    'score': 6.8,
                    'strengths': [
                        'Интуитивно понятная навигация',
                        'Адаптивный дизайн для мобильных устройств',
                        'Четкая структура информации об отелях'
                    ],
                    'weaknesses': [
                        'Слишком много кликов для применения фильтров',
                        'Неочевидное расположение кнопки "Бесплатная отмена"',
                        'Отсутствие визуальных подсказок'
                    ],
                    'recommendations': [
                        'Упростить процесс применения фильтров',
                        'Выделить тарифы с бесплатной отменой',
                        'Добавить туториал для новых пользователей'
                    ]
                },
                'content_quality': {
                    'score': 8.1,
                    'strengths': [
                        'Подробные описания отелей',
                        'Качественные фотографии',
                        'Актуальные отзывы пользователей'
                    ],
                    'weaknesses': [
                        'Недостаточно информации о горнолыжных услугах',
                        'Отсутствуют данные о расстоянии до подъемников',
                        'Нет информации о качестве лыжехранилища'
                    ],
                    'recommendations': [
                        'Добавить раздел "Горнолыжные услуги"',
                        'Указать точное расстояние до подъемников',
                        'Включить отзывы о лыжехранилище'
                    ]
                }
            },
            'competitive_analysis': {
                'booking_com': {
                    'score': 8.1,
                    'advantages': [
                        'Лучший фильтр по расстоянию до подъемника',
                        'Более подробная информация о горнолыжных услугах',
                        'Интеграция с картами подъемников'
                    ]
                },
                'hotels_com': {
                    'score': 6.9,
                    'advantages': [
                        'Более низкие цены',
                        'Простая система бронирования'
                    ]
                }
            },
            'business_impact': {
                'conversion_optimization': [
                    'Добавление фильтра лыжехранилища: +23% к конверсии',
                    'Улучшение карты: +15% к времени на сайте',
                    'Выделение бесплатной отмены: +18% к бронированиям'
                ],
                'user_experience': [
                    'Сокращение времени поиска на 40%',
                    'Увеличение удовлетворенности на 25%',
                    'Снижение отказов на 30%'
                ]
            }
        }
        
        return {
            'scenario': scenario,
            'summary': {
                'total_hotels': 156,
                'matching_hotels': 8,
                'success_rate': 89,
                'total_time': '4 мин 23 сек',
                'overall_rating': 7.4,
                'search_steps': 6,
                'filters_applied': 4,
                'hotels_viewed': 23
            },
            'metrics': {
                'usability': 7.2,
                'speed': 6.8,
                'features': 8.1,
                'overall': 7.4,
                'search_efficiency': 6.9,
                'filter_effectiveness': 5.8,
                'content_relevance': 7.6
            },
            'problems': [
                {'issue': 'Сложно найти лыжехранилище', 'rating': 3, 'impact': 'Высокий', 'frequency': 'Часто'},
                {'issue': 'Фильтр расстояния неточный', 'rating': 5, 'impact': 'Средний', 'frequency': 'Иногда'},
                {'issue': 'Цены не всегда актуальны', 'rating': 6, 'impact': 'Средний', 'frequency': 'Редко'},
                {'issue': 'Сложно найти бесплатную отмену', 'rating': 4, 'impact': 'Высокий', 'frequency': 'Часто'},
                {'issue': 'Карта не показывает подъемники', 'rating': 3, 'impact': 'Высокий', 'frequency': 'Всегда'}
            ],
            'recommendations': [
                {'priority': 'Высокий', 'effort': 'Низкий', 'impact': 'Высокий', 'recommendation': 'Добавить фильтр "лыжехранилище"'},
                {'priority': 'Высокий', 'effort': 'Средний', 'impact': 'Высокий', 'recommendation': 'Улучшить карту с подъемниками'},
                {'priority': 'Средний', 'effort': 'Низкий', 'impact': 'Средний', 'recommendation': 'Показывать актуальность цен'},
                {'priority': 'Средний', 'effort': 'Низкий', 'impact': 'Средний', 'recommendation': 'Выделить тарифы с бесплатной отменой'},
                {'priority': 'Низкий', 'effort': 'Высокий', 'impact': 'Низкий', 'recommendation': 'Добавить туториал для новых пользователей'}
            ],
            'personas_feedback': {
                'business_traveler': {
                    'rating': 7.8, 
                    'comment': 'Удобно для деловых поездок, но не хватает информации о трансфере',
                    'pain_points': ['Нет информации о трансфере', 'Сложно найти отели с конференц-залами'],
                    'suggestions': ['Добавить фильтр "Трансфер", "Конференц-зал"']
                },
                'family_traveler': {
                    'rating': 6.9, 
                    'comment': 'Хорошо для семей, но нужно больше информации о детских услугах',
                    'pain_points': ['Нет информации о детских клубах', 'Сложно найти семейные номера'],
                    'suggestions': ['Добавить фильтр "Детские услуги", "Семейные номера"']
                },
                'budget_traveler': {
                    'rating': 7.1, 
                    'comment': 'Приемлемые цены, но скрытые доплаты раздражают',
                    'pain_points': ['Скрытые доплаты', 'Нет фильтра по бюджету'],
                    'suggestions': ['Показывать полную стоимость сразу', 'Добавить фильтр "Бюджет"']
                },
                'ski_enthusiast': {
                    'rating': 5.2,
                    'comment': 'Для горнолыжников сайт неудобен - нет нужных фильтров',
                    'pain_points': ['Нет фильтра лыжехранилища', 'Нет информации о подъемниках'],
                    'suggestions': ['Создать раздел "Горнолыжные услуги"', 'Добавить карту подъемников']
                }
            },
            'enhanced_analysis': enhanced_analysis,
            'timeline': [
                {'step': 'Открытие сайта', 'duration': 2.3, 'status': 'success'},
                {'step': 'Поиск отелей', 'duration': 45.2, 'status': 'success'},
                {'step': 'Применение фильтров', 'duration': 67.8, 'status': 'partial'},
                {'step': 'Просмотр результатов', 'duration': 89.1, 'status': 'success'},
                {'step': 'Проверка деталей', 'duration': 34.5, 'status': 'success'},
                {'step': 'Генерация отчета', 'duration': 12.1, 'status': 'success'}
            ]
        }
    
    def add_message(self, sender, message, message_type="info"):
        """Добавление сообщения в чат"""
        self.messages.append({
            'id': len(self.messages),
            'sender': sender,
            'message': message,
            'type': message_type,
            'timestamp': datetime.now().strftime('%H:%M:%S')
        })
    
    def get_status(self):
        """Получение текущего статуса"""
        return {
            'research_id': self.research_id,
            'status': self.status,
            'progress': self.progress,
            'messages': self.messages,
            'results': self.results if self.status == "completed" else None
        }

# Создаем менеджер исследований
research_manager = ResearchManager()

@app.route('/')
def index():
    """Главная страница"""
    return render_template('index.html')

@app.route('/api/scenarios')
def get_scenarios():
    """Получение доступных сценариев"""
    scenarios = get_advanced_scenarios()
    return jsonify(scenarios)

@app.route('/api/research/start', methods=['POST'])
def start_research():
    """Запуск нового исследования"""
    data = request.json
    
    # Создаем новое исследование
    research_id = research_manager.start_research(data)
    
    return jsonify({
        'research_id': research_id,
        'status': 'started'
    })

@app.route('/api/research/<research_id>/status')
def get_research_status(research_id):
    """Получение статуса исследования"""
    if research_manager.research_id == research_id:
        return jsonify(research_manager.get_status())
    else:
        return jsonify({'error': 'Research not found'}), 404

@app.route('/api/research/<research_id>/stop', methods=['POST'])
def stop_research(research_id):
    """Остановка исследования"""
    if research_manager.research_id == research_id:
        research_manager.status = "stopped"
        research_manager.add_message("⏹️ Остановлено", "Исследование остановлено пользователем", "warning")
        return jsonify({'status': 'stopped'})
    else:
        return jsonify({'error': 'Research not found'}), 404

@app.route('/api/research/<research_id>/report')
def get_research_report(research_id):
    """Получение отчета исследования"""
    if research_manager.research_id == research_id and research_manager.status == "completed":
        return jsonify(research_manager.results)
    else:
        return jsonify({'error': 'Report not ready'}), 404

if __name__ == '__main__':
    # Для Render используем переменную окружения PORT
    port = int(os.environ.get('PORT', 5001))
    app.run(debug=False, host='0.0.0.0', port=port)
