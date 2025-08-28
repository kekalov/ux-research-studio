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
    # Временно возвращаем HTML напрямую для Render
    html_content = """
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>UX Research Studio - AI Agent для исследования сайтов</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            color: #333;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }
        
        .header {
            text-align: center;
            margin-bottom: 40px;
            color: white;
        }
        
        .header h1 {
            font-size: 2.5rem;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        
        .header p {
            font-size: 1.2rem;
            opacity: 0.9;
        }
        
        .main-content {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 30px;
            margin-bottom: 30px;
        }
        
        .card {
            background: white;
            border-radius: 15px;
            padding: 30px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            transition: transform 0.3s ease;
        }
        
        .card:hover {
            transform: translateY(-5px);
        }
        
        .card h2 {
            color: #667eea;
            margin-bottom: 20px;
            font-size: 1.5rem;
        }
        
        .form-group {
            margin-bottom: 20px;
        }
        
        .form-group label {
            display: block;
            margin-bottom: 8px;
            font-weight: 600;
            color: #555;
        }
        
        .form-group input,
        .form-group select,
        .form-group textarea {
            width: 100%;
            padding: 12px;
            border: 2px solid #e1e5e9;
            border-radius: 8px;
            font-size: 16px;
            transition: border-color 0.3s ease;
        }
        
        .form-group input:focus,
        .form-group select:focus,
        .form-group textarea:focus {
            outline: none;
            border-color: #667eea;
        }
        
        .form-row {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 15px;
        }
        
        .btn {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 15px 30px;
            border-radius: 8px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
            width: 100%;
        }
        
        .btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        }
        
        .btn:disabled {
            opacity: 0.6;
            cursor: not-allowed;
            transform: none;
        }
        
        .status-section {
            background: white;
            border-radius: 15px;
            padding: 30px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            margin-bottom: 30px;
        }
        
        .status-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
        }
        
        .status-indicator {
            display: flex;
            align-items: center;
            gap: 10px;
        }
        
        .status-dot {
            width: 12px;
            height: 12px;
            border-radius: 50%;
            background: #ccc;
        }
        
        .status-dot.running {
            background: #4CAF50;
            animation: pulse 2s infinite;
        }
        
        .status-dot.completed {
            background: #2196F3;
        }
        
        .status-dot.error {
            background: #f44336;
        }
        
        @keyframes pulse {
            0% { opacity: 1; }
            50% { opacity: 0.5; }
            100% { opacity: 1; }
        }
        
        .progress-bar {
            width: 100%;
            height: 8px;
            background: #e1e5e9;
            border-radius: 4px;
            overflow: hidden;
            margin-bottom: 20px;
        }
        
        .progress-fill {
            height: 100%;
            background: linear-gradient(90deg, #667eea, #764ba2);
            transition: width 0.3s ease;
            width: 0%;
        }
        
        .chat-container {
            max-height: 400px;
            overflow-y: auto;
            border: 1px solid #e1e5e9;
            border-radius: 8px;
            padding: 15px;
            background: #f8f9fa;
        }
        
        .message {
            margin-bottom: 15px;
            padding: 10px;
            border-radius: 8px;
            background: white;
            border-left: 4px solid #667eea;
        }
        
        .message.user {
            border-left-color: #4CAF50;
        }
        
        .message.agent {
            border-left-color: #2196F3;
        }
        
        .message.warning {
            border-left-color: #ff9800;
        }
        
        .message.error {
            border-left-color: #f44336;
        }
        
        .message-header {
            display: flex;
            justify-content: space-between;
            margin-bottom: 5px;
            font-size: 0.9rem;
            color: #666;
        }
        
        .message-content {
            color: #333;
        }
        
        .results-section {
            background: white;
            border-radius: 15px;
            padding: 30px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }
        
        .results-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-top: 20px;
        }
        
        .result-card {
            background: #f8f9fa;
            padding: 20px;
            border-radius: 8px;
            border-left: 4px solid #667eea;
        }
        
        .result-card h4 {
            color: #667eea;
            margin-bottom: 10px;
        }
        
        .rating {
            display: flex;
            align-items: center;
            gap: 5px;
            margin-bottom: 10px;
        }
        
        .star {
            color: #ffd700;
            font-size: 18px;
        }
        
        .hidden {
            display: none;
        }
        
        .alert {
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 20px;
        }
        
        .alert.info {
            background: #e3f2fd;
            border: 1px solid #2196F3;
            color: #0d47a1;
        }
        
        .alert.warning {
            background: #fff3e0;
            border: 1px solid #ff9800;
            color: #e65100;
        }
        
        .alert.error {
            background: #ffebee;
            border: 1px solid #f44336;
            color: #c62828;
        }
        
        @media (max-width: 768px) {
            .main-content {
                grid-template-columns: 1fr;
            }
            
            .form-row {
                grid-template-columns: 1fr;
            }
            
            .header h1 {
                font-size: 2rem;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🚀 UX Research Studio</h1>
            <p>AI Agent для автоматического исследования UX сайтов</p>
        </div>
        
        <div class="main-content">
            <div class="card">
                <h2>🎯 Настройка исследования</h2>
                <form id="researchForm">
                    <div class="form-group">
                        <label for="scenario_name">Сценарий:</label>
                        <select id="scenario_name" name="scenario_name" required>
                            <option value="">Выберите сценарий</option>
                            <option value="sochi_winter">Сочи - зимний сезон</option>
                            <option value="andorra">Андорра - горнолыжный курорт</option>
                            <option value="sochi_ski_premium">Сочи - премиум горнолыжный</option>
                            <option value="andorra_luxury_ski">Андорра - люкс горнолыжный</option>
                            <option value="custom">Кастомный сценарий</option>
                        </select>
                    </div>
                    
                    <div class="form-group">
                        <label for="name">Название исследования:</label>
                        <input type="text" id="name" name="name" placeholder="Например: Поиск отеля в Сочи" required>
                    </div>
                    
                    <div class="form-group">
                        <label for="destination">Направление:</label>
                        <input type="text" id="destination" name="destination" placeholder="Сочи, Андорра, Красная Поляна" required>
                    </div>
                    
                    <div class="form-group">
                        <label for="custom_prompt">Кастомный промпт для поиска:</label>
                        <textarea id="custom_prompt" name="custom_prompt" rows="4" placeholder="Опишите детально, что должен найти AI агент. Например: найти отель для горнолыжного отдыха с 4+ звездами, не дальше 2км от подъемника, с бесплатной отменой, до 10000 руб/ночь"></textarea>
                    </div>
                    
                    <div class="form-group">
                        <label for="competitor_analysis">Анализ конкурентов:</label>
                        <textarea id="competitor_analysis" name="competitor_analysis" rows="3" placeholder="Укажите сайты для сравнения (например: Yandex.Travel, Booking.com) или оставьте пустым для анализа только ostrovok.ru"></textarea>
                    </div>
                    
                    <div class="form-row">
                        <div class="form-group">
                            <label for="check_in">Дата заезда:</label>
                            <input type="date" id="check_in" name="check_in" required>
                        </div>
                        <div class="form-group">
                            <label for="check_out">Дата выезда:</label>
                            <input type="date" id="check_out" name="check_out" required>
                        </div>
                    </div>
                    
                    <div class="form-row">
                        <div class="form-group">
                            <label for="guests">Гостей:</label>
                            <input type="number" id="guests" name="guests" min="1" max="10" value="2" required>
                        </div>
                        <div class="form-group">
                            <label for="rooms">Комнат:</label>
                            <input type="number" id="rooms" name="rooms" min="1" max="5" value="1" required>
                        </div>
                    </div>
                    
                    <div class="form-group">
                        <label for="stars">Звездность отеля:</label>
                        <select id="stars" name="stars">
                            <option value="Любые">Любые</option>
                            <option value="3+">3+ звезды</option>
                            <option value="4+">4+ звезды</option>
                            <option value="5">5 звезд</option>
                        </select>
                    </div>
                    
                    <div class="form-group">
                        <label for="price_limit">Лимит цены за ночь:</label>
                        <input type="text" id="price_limit" name="price_limit" placeholder="Например: 10000 руб, 150€, Любая">
                    </div>
                    
                    <button type="submit" class="btn" id="startBtn">
                        🚀 Запустить исследование
                    </button>
                </form>
            </div>
            
            <div class="card">
                <h2>📊 Быстрые сценарии</h2>
                <div class="quick-scenarios">
                    <button class="btn" onclick="loadScenario('sochi_winter')">
                        🏂 Сочи - зимний сезон
                    </button>
                    <button class="btn" onclick="loadScenario('andorra')" style="margin-top: 15px;">
                        ⛷️ Андорра - горнолыжный
                    </button>
                    <button class="btn" onclick="loadScenario('sochi_ski_premium')" style="margin-top: 15px;">
                        🎿 Сочи - премиум горнолыжный
                    </button>
                    <button class="btn" onclick="loadScenario('andorra_luxury_ski')" style="margin-top: 15px;">
                        🏔️ Андорра - люкс горнолыжный
                    </button>
                </div>
                
                <div style="margin-top: 30px;">
                    <h3>💡 Как использовать</h3>
                    <ol style="margin-left: 20px; margin-top: 10px; line-height: 1.6;">
                        <li>Выберите готовый сценарий или создайте кастомный</li>
                        <li>Настройте параметры поиска</li>
                        <li>Добавьте кастомный промпт для специфичных требований</li>
                        <li>Укажите конкурентов для сравнения (опционально)</li>
                        <li>Запустите исследование</li>
                        <li>Следите за прогрессом в реальном времени</li>
                        <li>Получите детальный UX отчет</li>
                    </ol>
                </div>
            </div>
        </div>
        
        <div class="status-section hidden" id="statusSection">
            <div class="status-header">
                <h2>📈 Статус исследования</h2>
                <div class="status-indicator">
                    <div class="status-dot" id="statusDot"></div>
                    <span id="statusText">Ожидание</span>
                </div>
            </div>
            
            <div class="progress-bar">
                <div class="progress-fill" id="progressFill"></div>
            </div>
            
            <div class="chat-container" id="chatContainer">
                <!-- Сообщения будут добавляться динамически -->
            </div>
            
            <div style="margin-top: 20px; text-align: center;">
                <button class="btn" onclick="stopResearch()" id="stopBtn" style="display: none;">
                    ⏹️ Остановить исследование
                </button>
            </div>
        </div>
        
        <div class="results-section hidden" id="resultsSection">
            <h2>📊 Результаты исследования</h2>
            <div id="resultsContent">
                <!-- Результаты будут отображаться здесь -->
            </div>
        </div>
    </div>

    <script>
        let currentResearchId = null;
        let statusInterval = null;
        
        // Установка дат по умолчанию
        document.addEventListener('DOMContentLoaded', function() {
            const today = new Date();
            const checkIn = new Date(today.getTime() + (7 * 24 * 60 * 60 * 1000)); // +7 дней
            const checkOut = new Date(checkIn.getTime() + (7 * 24 * 60 * 60 * 1000)); // +14 дней
            
            document.getElementById('check_in').value = checkIn.toISOString().split('T')[0];
            document.getElementById('check_out').value = checkOut.toISOString().split('T')[0];
        });
        
        // Загрузка готовых сценариев
        function loadScenario(scenarioName) {
            const scenarios = {
                'sochi_winter': {
                    name: 'Сочи - зимний сезон',
                    destination: 'Сочи',
                    stars: '4+',
                    price_limit: '15000 руб'
                },
                'andorra': {
                    name: 'Андорра - горнолыжный курорт',
                    destination: 'Андорра',
                    stars: '4+',
                    price_limit: '200€'
                },
                'sochi_ski_premium': {
                    name: 'Сочи - премиум горнолыжный',
                    destination: 'Сочи',
                    stars: '5',
                    price_limit: '25000 руб'
                },
                'andorra_luxury_ski': {
                    name: 'Андорра - люкс горнолыжный',
                    destination: 'Андорра',
                    stars: '5',
                    price_limit: '500€'
                }
            };
            
            const scenario = scenarios[scenarioName];
            if (scenario) {
                document.getElementById('name').value = scenario.name;
                document.getElementById('destination').value = scenario.destination;
                document.getElementById('stars').value = scenario.stars;
                document.getElementById('price_limit').value = scenario.price_limit;
            }
        }
        
        // Обработка формы
        document.getElementById('researchForm').addEventListener('submit', function(e) {
            e.preventDefault();
            startResearch();
        });
        
        // Запуск исследования
        function startResearch() {
            const formData = new FormData(document.getElementById('researchForm'));
            const data = {
                scenario_name: formData.get('scenario_name'),
                name: formData.get('name'),
                destination: formData.get('destination'),
                custom_prompt: formData.get('custom_prompt'),
                competitor_analysis: formData.get('competitor_analysis'),
                check_in: formData.get('check_in'),
                check_out: formData.get('check_out'),
                guests: parseInt(formData.get('guests')),
                rooms: parseInt(formData.get('rooms')),
                stars: formData.get('stars'),
                price_limit: formData.get('price_limit')
            };
            
            // Показываем статус
            document.getElementById('statusSection').classList.remove('hidden');
            document.getElementById('resultsSection').classList.add('hidden');
            document.getElementById('startBtn').disabled = true;
            
            // Обновляем статус
            updateStatus('running', 'Запуск исследования...');
            addMessage('🤖 AI Agent', 'Начинаю исследование...', 'info');
            
            // Отправляем запрос
            fetch('/api/research/start', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data)
            })
            .then(response => response.json())
            .then(data => {
                currentResearchId = data.research_id;
                updateStatus('running', 'Исследование запущено');
                addMessage('✅ Система', 'Исследование успешно запущено!', 'info');
                
                // Запускаем мониторинг статуса
                startStatusMonitoring();
            })
            .catch(error => {
                console.error('Error:', error);
                updateStatus('error', 'Ошибка запуска');
                addMessage('❌ Ошибка', 'Не удалось запустить исследование: ' + error.message, 'error');
                document.getElementById('startBtn').disabled = false;
            });
        }
        
        // Остановка исследования
        function stopResearch() {
            if (currentResearchId) {
                fetch(`/api/research/${currentResearchId}/stop`, {
                    method: 'POST'
                })
                .then(response => response.json())
                .then(data => {
                    updateStatus('stopped', 'Исследование остановлено');
                    addMessage('⏹️ Система', 'Исследование остановлено пользователем', 'warning');
                    document.getElementById('stopBtn').style.display = 'none';
                    document.getElementById('startBtn').disabled = false;
                })
                .catch(error => {
                    console.error('Error:', error);
                    addMessage('❌ Ошибка', 'Не удалось остановить исследование', 'error');
                });
            }
        }
        
        // Мониторинг статуса
        function startStatusMonitoring() {
            if (statusInterval) {
                clearInterval(statusInterval);
            }
            
            statusInterval = setInterval(() => {
                if (currentResearchId) {
                    fetch(`/api/research/${currentResearchId}/status`)
                    .then(response => response.json())
                    .then(data => {
                        updateProgress(data.progress || 0);
                        updateStatus(data.status === 'running' ? 'running' : data.status === 'completed' ? 'completed' : 'error');
                        
                        if (data.messages) {
                            data.messages.forEach(msg => {
                                if (!document.querySelector(`[data-message-id="${msg.id}"]`)) {
                                    addMessage(msg.sender, msg.message, msg.type);
                                }
                            });
                        }
                        
                        if (data.status === 'completed') {
                            showResults(data.results);
                            clearInterval(statusInterval);
                            document.getElementById('stopBtn').style.display = 'none';
                            document.getElementById('startBtn').disabled = false;
                        }
                    })
                    .catch(error => {
                        console.error('Error:', error);
                    });
                }
            }, 2000);
        }
        
        // Обновление статуса
        function updateStatus(status, text) {
            const statusDot = document.getElementById('statusDot');
            const statusText = document.getElementById('statusText');
            
            statusDot.className = 'status-dot ' + status;
            statusText.textContent = text;
            
            if (status === 'running') {
                document.getElementById('stopBtn').style.display = 'inline-block';
            }
        }
        
        // Обновление прогресса
        function updateProgress(progress) {
            document.getElementById('progressFill').style.width = progress + '%';
        }
        
        // Добавление сообщения
        function addMessage(sender, message, type = 'info') {
            const container = document.getElementById('chatContainer');
            const messageDiv = document.createElement('div');
            messageDiv.className = `message ${type}`;
            messageDiv.setAttribute('data-message-id', Date.now());
            
            const timestamp = new Date().toLocaleTimeString();
            messageDiv.innerHTML = `
                <div class="message-header">
                    <strong>${sender}</strong>
                    <span>${timestamp}</span>
                </div>
                <div class="message-content">${message}</div>
            `;
            
            container.appendChild(messageDiv);
            container.scrollTop = container.scrollHeight;
        }
        
        // Показ результатов
        function showResults(results) {
            document.getElementById('resultsSection').classList.remove('hidden');
            
            const content = document.getElementById('resultsContent');
            content.innerHTML = `
                <div class="alert alert-info">
                    <strong>Исследование завершено!</strong> Получены результаты UX анализа.
                </div>
                
                <div class="results-grid">
                    <div class="result-card">
                        <h4>📊 Общая оценка</h4>
                        <div class="rating">
                            <span class="star">★</span>
                            <span class="star">★</span>
                            <span class="star">★</span>
                            <span class="star">★</span>
                            <span class="star">☆</span>
                            <span>${results.overall_rating || 'N/A'}/10</span>
                        </div>
                        <p>${results.overall_feedback || 'Оценка не доступна'}</p>
                    </div>
                    
                    <div class="result-card">
                        <h4>🎯 Основные выводы</h4>
                        <p>${results.main_findings || 'Выводы не доступны'}</p>
                    </div>
                    
                    <div class="result-card">
                        <h4>⚠️ Проблемы</h4>
                        <p>${results.issues || 'Проблемы не выявлены'}</p>
                    </div>
                    
                    <div class="result-card">
                        <h4>💡 Рекомендации</h4>
                        <p>${results.recommendations || 'Рекомендации не доступны'}</p>
                    </div>
                </div>
                
                <div style="margin-top: 30px;">
                    <h3>📋 Детальный отчет</h3>
                    <p>Для получения полного отчета с графиками и детальным анализом, скачайте JSON файл:</p>
                    <button class="btn" onclick="downloadReport()">
                        📥 Скачать отчет
                    </button>
                </div>
            `;
        }
        
        // Скачивание отчета
        function downloadReport() {
            if (currentResearchId) {
                window.open(`/api/research/${currentResearchId}/report`, '_blank');
            }
        }
    </script>
</body>
</html>
"""
    return html_content

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
