"""
User Simulator - модуль для симуляции поведения реального пользователя
"""

import time
import random
import logging
from typing import Dict, Any, List
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

logger = logging.getLogger(__name__)

class UserSimulator:
    """Симулятор поведения реального пользователя"""
    
    def __init__(self):
        self.user_behavior = {
            'reading_time': (2, 5),  # Время на чтение (сек)
            'thinking_time': (1, 3),  # Время на размышление (сек)
            'typing_speed': (0.1, 0.3),  # Скорость печати (сек на символ)
            'scroll_probability': 0.7,  # Вероятность прокрутки
            'hover_probability': 0.6,  # Вероятность наведения мыши
            'mistake_probability': 0.1,  # Вероятность ошибки
        }
        
    def simulate_human_behavior(self, driver: WebDriver, action: str, **kwargs):
        """Симуляция человеческого поведения"""
        
        # Случайная задержка перед действием
        thinking_time = random.uniform(*self.user_behavior['thinking_time'])
        time.sleep(thinking_time)
        
        # Симуляция конкретного действия
        if action == 'type':
            self._simulate_typing(driver, kwargs.get('element'), kwargs.get('text', ''))
        elif action == 'click':
            self._simulate_click(driver, kwargs.get('element'))
        elif action == 'scroll':
            self._simulate_scroll(driver)
        elif action == 'hover':
            self._simulate_hover(driver, kwargs.get('element'))
        elif action == 'read':
            self._simulate_reading(driver, kwargs.get('duration', 3))
        elif action == 'explore':
            self._simulate_exploration(driver)
            
    def _simulate_typing(self, driver: WebDriver, element, text: str):
        """Симуляция человеческой печати"""
        if not element or not text:
            return
            
        # Очистка поля
        element.clear()
        time.sleep(0.5)
        
        # Печать текста с человеческой скоростью
        for char in text:
            element.send_keys(char)
            typing_delay = random.uniform(*self.user_behavior['typing_speed'])
            time.sleep(typing_delay)
            
        # Пауза после печати
        time.sleep(random.uniform(0.5, 1.5))
        
    def _simulate_click(self, driver: WebDriver, element):
        """Симуляция человеческого клика"""
        if not element:
            return
            
        # Наведение мыши перед кликом
        actions = ActionChains(driver)
        actions.move_to_element(element)
        actions.pause(random.uniform(0.2, 0.8))
        actions.click()
        actions.perform()
        
        # Пауза после клика
        time.sleep(random.uniform(0.5, 2.0))
        
    def _simulate_scroll(self, driver: WebDriver):
        """Симуляция прокрутки страницы"""
        if random.random() < self.user_behavior['scroll_probability']:
            scroll_amount = random.randint(300, 800)
            driver.execute_script(f"window.scrollBy(0, {scroll_amount});")
            time.sleep(random.uniform(1, 3))
            
    def _simulate_hover(self, driver: WebDriver, element):
        """Симуляция наведения мыши"""
        if element and random.random() < self.user_behavior['hover_probability']:
            actions = ActionChains(driver)
            actions.move_to_element(element)
            actions.pause(random.uniform(0.5, 2.0))
            actions.perform()
            
    def _simulate_reading(self, driver: WebDriver, duration: int = 3):
        """Симуляция чтения контента"""
        reading_time = random.uniform(duration * 0.7, duration * 1.3)
        time.sleep(reading_time)
        
    def _simulate_exploration(self, driver: WebDriver):
        """Симуляция исследования страницы"""
        # Случайная прокрутка
        self._simulate_scroll(driver)
        
        # Поиск интересных элементов
        interesting_elements = driver.find_elements(By.CSS_SELECTOR, 
            'a, button, .hotel-card, .filter, .price, .rating')
        
        if interesting_elements:
            # Наведение на случайный элемент
            random_element = random.choice(interesting_elements[:5])
            self._simulate_hover(driver, random_element)
            
    def simulate_user_decision_making(self, options: List[str], context: str) -> str:
        """Симуляция принятия решений пользователем"""
        
        # Логика принятия решений в зависимости от контекста
        if context == 'destination':
            # Пользователь может выбрать популярное направление
            popular_destinations = ['Сочи', 'Андорра', 'Москва', 'Санкт-Петербург']
            return random.choice(popular_destinations)
            
        elif context == 'dates':
            # Пользователь выбирает даты для зимнего отдыха
            winter_dates = [
                ('2024-12-20', '2024-12-27'),
                ('2024-12-25', '2025-01-02'),
                ('2025-01-15', '2025-01-22'),
                ('2025-02-01', '2025-02-08')
            ]
            return random.choice(winter_dates)
            
        elif context == 'guests':
            # Типичные комбинации гостей
            guest_combinations = [(1, 1), (2, 1), (2, 2), (3, 1), (4, 2)]
            return random.choice(guest_combinations)
            
        elif context == 'filters':
            # Пользователь применяет популярные фильтры
            common_filters = ['Цена', 'Звезды', 'Wi-Fi', 'Парковка', 'Бассейн']
            return random.choice(common_filters)
            
        else:
            return random.choice(options) if options else ''
            
    def simulate_user_frustration(self, driver: WebDriver, issue: str):
        """Симуляция фрустрации пользователя"""
        
        logger.info(f"Пользователь испытывает фрустрацию: {issue}")
        
        # Поведение при фрустрации
        behaviors = [
            'multiple_clicks',  # Множественные клики
            'page_refresh',     # Обновление страницы
            'go_back',          # Возврат назад
            'try_alternative'   # Попытка альтернативного пути
        ]
        
        behavior = random.choice(behaviors)
        
        if behavior == 'multiple_clicks':
            # Множественные клики на элемент
            elements = driver.find_elements(By.CSS_SELECTOR, 'button, a')
            if elements:
                for _ in range(random.randint(2, 4)):
                    self._simulate_click(driver, random.choice(elements))
                    
        elif behavior == 'page_refresh':
            # Обновление страницы
            driver.refresh()
            time.sleep(random.uniform(2, 4))
            
        elif behavior == 'go_back':
            # Возврат назад
            driver.back()
            time.sleep(random.uniform(1, 3))
            
    def generate_user_feedback(self, journey_data: Dict[str, Any]) -> Dict[str, Any]:
        """Генерация фидбэка от лица пользователя"""
        
        steps = journey_data.get('steps', [])
        successful_steps = [s for s in steps if s.get('success', False)]
        failed_steps = [s for s in steps if not s.get('success', False)]
        
        feedback = {
            'overall_experience': self._evaluate_overall_experience(journey_data),
            'task_completion': self._evaluate_task_completion(journey_data),
            'usability_issues': self._identify_usability_issues(failed_steps),
            'positive_aspects': self._identify_positive_aspects(successful_steps),
            'recommendations': self._generate_recommendations(journey_data),
            'emotional_response': self._simulate_emotional_response(journey_data)
        }
        
        return feedback
        
    def _evaluate_overall_experience(self, journey_data: Dict[str, Any]) -> Dict[str, Any]:
        """Оценка общего опыта"""
        
        total_time = sum(step.get('duration', 0) for step in journey_data.get('steps', []))
        success_rate = len([s for s in journey_data.get('steps', []) if s.get('success', False)]) / len(journey_data.get('steps', [])) if journey_data.get('steps') else 0
        
        # Оценка по шкале 1-10
        if success_rate >= 0.9 and total_time < 30:
            rating = random.randint(8, 10)
            experience = "Отличный"
        elif success_rate >= 0.7 and total_time < 60:
            rating = random.randint(6, 8)
            experience = "Хороший"
        elif success_rate >= 0.5:
            rating = random.randint(4, 6)
            experience = "Удовлетворительный"
        else:
            rating = random.randint(1, 4)
            experience = "Плохой"
            
        return {
            'rating': rating,
            'experience': experience,
            'total_time': total_time,
            'success_rate': success_rate
        }
        
    def _evaluate_task_completion(self, journey_data: Dict[str, Any]) -> Dict[str, Any]:
        """Оценка выполнения задачи"""
        
        steps = journey_data.get('steps', [])
        
        # Проверяем ключевые шаги
        key_actions = ['search_destination', 'select_dates', 'search_hotels', 'analyze_search_results']
        completed_key_actions = [action for action in key_actions 
                               if any(step.get('action') == action and step.get('success') 
                                     for step in steps)]
        
        task_completion_rate = len(completed_key_actions) / len(key_actions)
        
        return {
            'completed': task_completion_rate >= 0.75,
            'completion_rate': task_completion_rate,
            'missing_actions': [action for action in key_actions if action not in completed_key_actions]
        }
        
    def _identify_usability_issues(self, failed_steps: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Выявление проблем с удобством использования"""
        
        issues = []
        
        for step in failed_steps:
            action = step.get('action', '')
            error = step.get('error', '')
            duration = step.get('duration', 0)
            
            if 'search_destination' in action:
                issues.append({
                    'type': 'navigation',
                    'description': 'Сложно найти поле поиска или ввести направление',
                    'severity': 'high',
                    'suggestion': 'Сделать поле поиска более заметным'
                })
            elif 'select_dates' in action:
                issues.append({
                    'type': 'date_selection',
                    'description': 'Проблемы с выбором дат',
                    'severity': 'medium',
                    'suggestion': 'Упростить календарь'
                })
            elif 'filters' in action:
                issues.append({
                    'type': 'filtering',
                    'description': 'Фильтры работают нестабильно',
                    'severity': 'medium',
                    'suggestion': 'Исправить функциональность фильтров'
                })
            elif duration > 10:
                issues.append({
                    'type': 'performance',
                    'description': f'Долгое время выполнения: {duration} сек',
                    'severity': 'high',
                    'suggestion': 'Оптимизировать производительность'
                })
                
        return issues
        
    def _identify_positive_aspects(self, successful_steps: List[Dict[str, Any]]) -> List[str]:
        """Выявление положительных аспектов"""
        
        positive_aspects = []
        
        for step in successful_steps:
            action = step.get('action', '')
            duration = step.get('duration', 0)
            
            if 'search_destination' in action and duration < 3:
                positive_aspects.append('Быстрый поиск направления')
            elif 'search_hotels' in action:
                positive_aspects.append('Быстрый поиск отелей')
            elif 'analyze_search_results' in action:
                analysis = step.get('analysis', {})
                if analysis.get('hotels_count', 0) > 20:
                    positive_aspects.append('Большой выбор отелей')
                if analysis.get('filters_available'):
                    positive_aspects.append('Хороший набор фильтров')
                    
        return positive_aspects
        
    def _generate_recommendations(self, journey_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Генерация рекомендаций"""
        
        recommendations = []
        issues = self._identify_usability_issues([s for s in journey_data.get('steps', []) if not s.get('success', False)])
        
        for issue in issues:
            recommendations.append({
                'priority': issue['severity'],
                'category': issue['type'],
                'description': issue['suggestion'],
                'impact': 'high' if issue['severity'] == 'high' else 'medium'
            })
            
        # Общие рекомендации
        overall_experience = self._evaluate_overall_experience(journey_data)
        if overall_experience['rating'] < 7:
            recommendations.append({
                'priority': 'high',
                'category': 'general',
                'description': 'Провести полный UX-аудит сайта',
                'impact': 'high'
            })
            
        return recommendations
        
    def _simulate_emotional_response(self, journey_data: Dict[str, Any]) -> Dict[str, Any]:
        """Симуляция эмоциональной реакции пользователя"""
        
        overall_experience = self._evaluate_overall_experience(journey_data)
        rating = overall_experience['rating']
        
        if rating >= 8:
            emotions = ['доволен', 'удовлетворен', 'восторжен']
            confidence = 'высокая'
        elif rating >= 6:
            emotions = ['нейтрален', 'спокоен', 'заинтересован']
            confidence = 'средняя'
        elif rating >= 4:
            emotions = ['разочарован', 'озадачен', 'напряжен']
            confidence = 'низкая'
        else:
            emotions = ['раздражен', 'расстроен', 'зол']
            confidence = 'очень низкая'
            
        return {
            'primary_emotion': random.choice(emotions),
            'confidence_level': confidence,
            'would_recommend': rating >= 6,
            'would_return': rating >= 5
        }


