"""
AI UX Research Agent - основной класс для исследования пользовательского опыта
"""

import time
import logging
from typing import Dict, Any, List
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from fake_useragent import UserAgent

from .web_analyzer import WebAnalyzer
from .ai_analyzer import AIAnalyzer
from .scenario_executor import ScenarioExecutor
from .user_simulator import UserSimulator

logger = logging.getLogger(__name__)

class UXResearchAgent:
    """AI агент для UX-исследования"""
    
    def __init__(self, config: Dict[str, Any], headless: bool = False):
        self.config = config
        self.headless = headless
        self.driver = None
        self.web_analyzer = WebAnalyzer()
        self.ai_analyzer = AIAnalyzer(config['ai'])
        self.scenario_executor = ScenarioExecutor()
        self.user_simulator = UserSimulator()
        
    def __enter__(self):
        self.setup_driver()
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cleanup()
        
    def setup_driver(self):
        """Настройка веб-драйвера"""
        try:
            chrome_options = Options()
            
            if self.headless:
                chrome_options.add_argument('--headless')
            
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument('--window-size=1920,1080')
            chrome_options.add_argument(f'--user-agent={self.config["user_agent"]}')
            
            # Отключение изображений для ускорения
            chrome_options.add_argument('--blink-settings=imagesEnabled=false')
            
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            
            # Настройка таймаутов
            self.driver.implicitly_wait(self.config['browser']['implicit_wait'])
            self.driver.set_page_load_timeout(self.config['browser']['page_load_timeout'])
            
            logger.info("Веб-драйвер успешно инициализирован")
            
        except Exception as e:
            logger.error(f"Ошибка при инициализации драйвера: {e}")
            raise
            
    def cleanup(self):
        """Очистка ресурсов"""
        if self.driver:
            self.driver.quit()
            logger.info("Веб-драйвер закрыт")
            
    def run_scenario(self, scenario_name: str) -> Dict[str, Any]:
        """Выполнение сценария исследования"""
        
        logger.info(f"Запуск сценария: {scenario_name}")
        
        scenario_config = self.config['scenarios'].get(scenario_name)
        if not scenario_config:
            raise ValueError(f"Неизвестный сценарий: {scenario_name}")
            
        results = {
            'scenario': scenario_name,
            'timestamp': time.time(),
            'config': scenario_config,
            'steps': [],
            'analysis': {},
            'screenshots': []
        }
        
        try:
            # Переход на главную страницу
            self.navigate_to_homepage()
            
            # Выполнение сценария
            if scenario_name == 'sochi_winter':
                results = self.execute_sochi_scenario(results)
            elif scenario_name == 'andorra':
                results = self.execute_andorra_scenario(results)
            elif scenario_name == 'full_analysis':
                results = self.execute_full_analysis(results)
                
            # AI анализ результатов
            results['analysis'] = self.ai_analyzer.analyze_results(results)
            
        except Exception as e:
            logger.error(f"Ошибка при выполнении сценария: {e}")
            results['error'] = str(e)
            
        return results
        
    def navigate_to_homepage(self):
        """Переход на главную страницу"""
        logger.info("Переход на главную страницу Ostrovok.ru")
        self.driver.get(self.config['base_url'])
        time.sleep(self.config['delays']['page_load'])
        
    def execute_sochi_scenario(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Выполнение сценария поиска отелей в Сочи"""
        
        scenario_config = self.config['scenarios']['sochi_winter']
        
        # Шаг 1: Поиск направления
        step1 = self.search_destination(scenario_config['destination'])
        results['steps'].append(step1)
        
        # Шаг 2: Выбор дат
        step2 = self.select_dates(scenario_config['check_in'], scenario_config['check_out'])
        results['steps'].append(step2)
        
        # Шаг 3: Настройка гостей
        step3 = self.configure_guests(scenario_config['guests'], scenario_config['rooms'])
        results['steps'].append(step3)
        
        # Шаг 4: Поиск отелей
        step4 = self.search_hotels()
        results['steps'].append(step4)
        
        # Шаг 5: Анализ результатов
        step5 = self.analyze_search_results()
        results['steps'].append(step5)
        
        return results
        
    def execute_andorra_scenario(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Выполнение сценария поиска отелей в Андорре"""
        
        scenario_config = self.config['scenarios']['andorra']
        
        # Аналогичные шаги для Андорры
        step1 = self.search_destination(scenario_config['destination'])
        results['steps'].append(step1)
        
        step2 = self.select_dates(scenario_config['check_in'], scenario_config['check_out'])
        results['steps'].append(step2)
        
        step3 = self.configure_guests(scenario_config['guests'], scenario_config['rooms'])
        results['steps'].append(step3)
        
        step4 = self.search_hotels()
        results['steps'].append(step4)
        
        step5 = self.analyze_search_results()
        results['steps'].append(step5)
        
        return results
        
    def execute_full_analysis(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Полный анализ всех функций сайта"""
        
        # Анализ главной страницы
        step1 = self.analyze_homepage()
        results['steps'].append(step1)
        
        # Анализ поиска
        step2 = self.analyze_search_functionality()
        results['steps'].append(step2)
        
        # Анализ фильтров
        step3 = self.analyze_filters()
        results['steps'].append(step3)
        
        # Анализ процесса бронирования
        step4 = self.analyze_booking_process()
        results['steps'].append(step4)
        
        return results
        
    def search_destination(self, destination: str) -> Dict[str, Any]:
        """Поиск направления"""
        logger.info(f"Поиск направления: {destination}")
        
        try:
            # Поиск поля ввода
            search_box = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, self.config['selectors']['search_box']))
            )
            
            # Очистка поля и ввод направления
            search_box.clear()
            search_box.send_keys(destination)
            time.sleep(self.config['delays']['user_action'])
            
            # Выбор первого предложения (если есть)
            suggestions = self.driver.find_elements(By.CSS_SELECTOR, '.suggestion-item')
            if suggestions:
                suggestions[0].click()
                
            return {
                'action': 'search_destination',
                'destination': destination,
                'success': True,
                'timestamp': time.time()
            }
            
        except Exception as e:
            logger.error(f"Ошибка при поиске направления: {e}")
            return {
                'action': 'search_destination',
                'destination': destination,
                'success': False,
                'error': str(e),
                'timestamp': time.time()
            }
            
    def select_dates(self, check_in: str, check_out: str) -> Dict[str, Any]:
        """Выбор дат заезда и выезда"""
        logger.info(f"Выбор дат: {check_in} - {check_out}")
        
        try:
            # Здесь будет логика выбора дат
            # Пока заглушка
            time.sleep(self.config['delays']['user_action'])
            
            return {
                'action': 'select_dates',
                'check_in': check_in,
                'check_out': check_out,
                'success': True,
                'timestamp': time.time()
            }
            
        except Exception as e:
            logger.error(f"Ошибка при выборе дат: {e}")
            return {
                'action': 'select_dates',
                'check_in': check_in,
                'check_out': check_out,
                'success': False,
                'error': str(e),
                'timestamp': time.time()
            }
            
    def configure_guests(self, guests: int, rooms: int) -> Dict[str, Any]:
        """Настройка количества гостей и комнат"""
        logger.info(f"Настройка гостей: {guests}, комнат: {rooms}")
        
        try:
            # Здесь будет логика настройки гостей
            time.sleep(self.config['delays']['user_action'])
            
            return {
                'action': 'configure_guests',
                'guests': guests,
                'rooms': rooms,
                'success': True,
                'timestamp': time.time()
            }
            
        except Exception as e:
            logger.error(f"Ошибка при настройке гостей: {e}")
            return {
                'action': 'configure_guests',
                'guests': guests,
                'rooms': rooms,
                'success': False,
                'error': str(e),
                'timestamp': time.time()
            }
            
    def search_hotels(self) -> Dict[str, Any]:
        """Поиск отелей"""
        logger.info("Поиск отелей")
        
        try:
            # Нажатие кнопки поиска
            search_button = self.driver.find_element(By.CSS_SELECTOR, self.config['selectors']['search_button'])
            search_button.click()
            
            # Ожидание загрузки результатов
            time.sleep(self.config['delays']['page_load'])
            
            return {
                'action': 'search_hotels',
                'success': True,
                'timestamp': time.time()
            }
            
        except Exception as e:
            logger.error(f"Ошибка при поиске отелей: {e}")
            return {
                'action': 'search_hotels',
                'success': False,
                'error': str(e),
                'timestamp': time.time()
            }
            
    def analyze_search_results(self) -> Dict[str, Any]:
        """Анализ результатов поиска"""
        logger.info("Анализ результатов поиска")
        
        try:
            # Получение HTML страницы
            page_source = self.driver.page_source
            
            # Анализ с помощью WebAnalyzer
            analysis = self.web_analyzer.analyze_search_results(page_source)
            
            # Создание скриншота
            screenshot_path = f"screenshots/search_results_{int(time.time())}.png"
            self.driver.save_screenshot(screenshot_path)
            
            return {
                'action': 'analyze_search_results',
                'analysis': analysis,
                'screenshot': screenshot_path,
                'success': True,
                'timestamp': time.time()
            }
            
        except Exception as e:
            logger.error(f"Ошибка при анализе результатов: {e}")
            return {
                'action': 'analyze_search_results',
                'success': False,
                'error': str(e),
                'timestamp': time.time()
            }
            
    def analyze_homepage(self) -> Dict[str, Any]:
        """Анализ главной страницы"""
        logger.info("Анализ главной страницы")
        
        try:
            page_source = self.driver.page_source
            analysis = self.web_analyzer.analyze_homepage(page_source)
            
            screenshot_path = f"screenshots/homepage_{int(time.time())}.png"
            self.driver.save_screenshot(screenshot_path)
            
            return {
                'action': 'analyze_homepage',
                'analysis': analysis,
                'screenshot': screenshot_path,
                'success': True,
                'timestamp': time.time()
            }
            
        except Exception as e:
            logger.error(f"Ошибка при анализе главной страницы: {e}")
            return {
                'action': 'analyze_homepage',
                'success': False,
                'error': str(e),
                'timestamp': time.time()
            }
            
    def analyze_search_functionality(self) -> Dict[str, Any]:
        """Анализ функциональности поиска"""
        logger.info("Анализ функциональности поиска")
        
        try:
            # Анализ элементов поиска
            search_elements = self.web_analyzer.analyze_search_elements(self.driver)
            
            return {
                'action': 'analyze_search_functionality',
                'analysis': search_elements,
                'success': True,
                'timestamp': time.time()
            }
            
        except Exception as e:
            logger.error(f"Ошибка при анализе поиска: {e}")
            return {
                'action': 'analyze_search_functionality',
                'success': False,
                'error': str(e),
                'timestamp': time.time()
            }
            
    def analyze_filters(self) -> Dict[str, Any]:
        """Анализ фильтров"""
        logger.info("Анализ фильтров")
        
        try:
            # Анализ доступных фильтров
            filters_analysis = self.web_analyzer.analyze_filters(self.driver)
            
            return {
                'action': 'analyze_filters',
                'analysis': filters_analysis,
                'success': True,
                'timestamp': time.time()
            }
            
        except Exception as e:
            logger.error(f"Ошибка при анализе фильтров: {e}")
            return {
                'action': 'analyze_filters',
                'success': False,
                'error': str(e),
                'timestamp': time.time()
            }
            
    def analyze_booking_process(self) -> Dict[str, Any]:
        """Анализ процесса бронирования"""
        logger.info("Анализ процесса бронирования")
        
        try:
            # Анализ процесса бронирования
            booking_analysis = self.web_analyzer.analyze_booking_process(self.driver)
            
            return {
                'action': 'analyze_booking_process',
                'analysis': booking_analysis,
                'success': True,
                'timestamp': time.time()
            }
            
        except Exception as e:
            logger.error(f"Ошибка при анализе бронирования: {e}")
            return {
                'action': 'analyze_booking_process',
                'success': False,
                'error': str(e),
                'timestamp': time.time()
            }
