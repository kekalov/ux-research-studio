"""
Scenario Executor - модуль для выполнения пользовательских сценариев
"""

import time
import logging
from typing import Dict, Any, List
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

logger = logging.getLogger(__name__)

class ScenarioExecutor:
    """Исполнитель сценариев пользовательского опыта"""
    
    def __init__(self):
        self.wait_timeout = 10
        
    def execute_search_scenario(self, driver: WebDriver, scenario_config: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Выполнение сценария поиска отелей"""
        
        steps = []
        
        try:
            # Шаг 1: Поиск направления
            step1 = self._search_destination(driver, scenario_config['destination'])
            steps.append(step1)
            
            if not step1['success']:
                return steps
                
            # Шаг 2: Выбор дат
            step2 = self._select_dates(driver, scenario_config['check_in'], scenario_config['check_out'])
            steps.append(step2)
            
            if not step2['success']:
                return steps
                
            # Шаг 3: Настройка гостей
            step3 = self._configure_guests(driver, scenario_config['guests'], scenario_config['rooms'])
            steps.append(step3)
            
            if not step3['success']:
                return steps
                
            # Шаг 4: Поиск отелей
            step4 = self._search_hotels(driver)
            steps.append(step4)
            
            if not step4['success']:
                return steps
                
            # Шаг 5: Анализ результатов
            step5 = self._analyze_results(driver)
            steps.append(step5)
            
        except Exception as e:
            logger.error(f"Ошибка при выполнении сценария поиска: {e}")
            steps.append({
                'action': 'scenario_execution',
                'success': False,
                'error': str(e),
                'timestamp': time.time()
            })
            
        return steps
        
    def execute_filtering_scenario(self, driver: WebDriver) -> List[Dict[str, Any]]:
        """Выполнение сценария работы с фильтрами"""
        
        steps = []
        
        try:
            # Шаг 1: Анализ доступных фильтров
            step1 = self._analyze_available_filters(driver)
            steps.append(step1)
            
            # Шаг 2: Применение фильтра по цене
            step2 = self._apply_price_filter(driver)
            steps.append(step2)
            
            # Шаг 3: Применение фильтра по звездам
            step3 = self._apply_star_filter(driver)
            steps.append(step3)
            
            # Шаг 4: Применение фильтра по удобствам
            step4 = self._apply_amenity_filter(driver)
            steps.append(step4)
            
            # Шаг 5: Анализ результатов фильтрации
            step5 = self._analyze_filtered_results(driver)
            steps.append(step5)
            
        except Exception as e:
            logger.error(f"Ошибка при выполнении сценария фильтрации: {e}")
            steps.append({
                'action': 'filtering_scenario',
                'success': False,
                'error': str(e),
                'timestamp': time.time()
            })
            
        return steps
        
    def execute_booking_scenario(self, driver: WebDriver) -> List[Dict[str, Any]]:
        """Выполнение сценария бронирования"""
        
        steps = []
        
        try:
            # Шаг 1: Выбор отеля
            step1 = self._select_hotel(driver)
            steps.append(step1)
            
            if not step1['success']:
                return steps
                
            # Шаг 2: Выбор номера
            step2 = self._select_room(driver)
            steps.append(step2)
            
            if not step2['success']:
                return steps
                
            # Шаг 3: Заполнение данных гостей
            step3 = self._fill_guest_info(driver)
            steps.append(step3)
            
            if not step3['success']:
                return steps
                
            # Шаг 4: Анализ процесса оплаты
            step4 = self._analyze_payment_process(driver)
            steps.append(step4)
            
        except Exception as e:
            logger.error(f"Ошибка при выполнении сценария бронирования: {e}")
            steps.append({
                'action': 'booking_scenario',
                'success': False,
                'error': str(e),
                'timestamp': time.time()
            })
            
        return steps
        
    def _search_destination(self, driver: WebDriver, destination: str) -> Dict[str, Any]:
        """Поиск направления"""
        start_time = time.time()
        
        try:
            logger.info(f"Поиск направления: {destination}")
            
            # Поиск поля ввода
            search_selectors = [
                'input[name*="query"]',
                'input[placeholder*="поиск"]',
                'input[placeholder*="куда"]',
                '.search-input',
                '#search-input'
            ]
            
            search_box = None
            for selector in search_selectors:
                try:
                    search_box = WebDriverWait(driver, 5).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                    )
                    break
                except:
                    continue
                    
            if not search_box:
                return {
                    'action': 'search_destination',
                    'destination': destination,
                    'success': False,
                    'error': 'Поле поиска не найдено',
                    'timestamp': time.time(),
                    'duration': time.time() - start_time
                }
                
            # Очистка поля и ввод направления
            search_box.clear()
            search_box.send_keys(destination)
            time.sleep(1)
            
            # Ожидание появления предложений
            try:
                suggestions = WebDriverWait(driver, 3).until(
                    EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.suggestion, .autocomplete-item, .dropdown-item'))
                )
                
                if suggestions:
                    suggestions[0].click()
                    time.sleep(1)
                    
            except:
                # Если предложения не появились, нажимаем Enter
                search_box.send_keys(Keys.ENTER)
                time.sleep(1)
                
            return {
                'action': 'search_destination',
                'destination': destination,
                'success': True,
                'timestamp': time.time(),
                'duration': time.time() - start_time
            }
            
        except Exception as e:
            logger.error(f"Ошибка при поиске направления: {e}")
            return {
                'action': 'search_destination',
                'destination': destination,
                'success': False,
                'error': str(e),
                'timestamp': time.time(),
                'duration': time.time() - start_time
            }
            
    def _select_dates(self, driver: WebDriver, check_in: str, check_out: str) -> Dict[str, Any]:
        """Выбор дат заезда и выезда"""
        start_time = time.time()
        
        try:
            logger.info(f"Выбор дат: {check_in} - {check_out}")
            
            # Поиск полей дат
            date_selectors = [
                'input[type="date"]',
                '.date-picker input',
                '.check-in input',
                '.check-out input'
            ]
            
            date_inputs = []
            for selector in date_selectors:
                try:
                    inputs = driver.find_elements(By.CSS_SELECTOR, selector)
                    date_inputs.extend(inputs)
                except:
                    continue
                    
            if len(date_inputs) >= 2:
                # Заполнение даты заезда
                date_inputs[0].clear()
                date_inputs[0].send_keys(check_in)
                time.sleep(0.5)
                
                # Заполнение даты выезда
                date_inputs[1].clear()
                date_inputs[1].send_keys(check_out)
                time.sleep(0.5)
                
            else:
                # Альтернативный способ - клик по календарю
                calendar_selectors = [
                    '.date-picker',
                    '.calendar',
                    '.date-selector'
                ]
                
                for selector in calendar_selectors:
                    try:
                        calendar = driver.find_element(By.CSS_SELECTOR, selector)
                        calendar.click()
                        time.sleep(1)
                        break
                    except:
                        continue
                        
            return {
                'action': 'select_dates',
                'check_in': check_in,
                'check_out': check_out,
                'success': True,
                'timestamp': time.time(),
                'duration': time.time() - start_time
            }
            
        except Exception as e:
            logger.error(f"Ошибка при выборе дат: {e}")
            return {
                'action': 'select_dates',
                'check_in': check_in,
                'check_out': check_out,
                'success': False,
                'error': str(e),
                'timestamp': time.time(),
                'duration': time.time() - start_time
            }
            
    def _configure_guests(self, driver: WebDriver, guests: int, rooms: int) -> Dict[str, Any]:
        """Настройка количества гостей и комнат"""
        start_time = time.time()
        
        try:
            logger.info(f"Настройка гостей: {guests}, комнат: {rooms}")
            
            # Поиск селекторов гостей
            guest_selectors = [
                '.guest-selector',
                '.traveler-selector',
                '.guests-input',
                '.rooms-input'
            ]
            
            for selector in guest_selectors:
                try:
                    guest_element = driver.find_element(By.CSS_SELECTOR, selector)
                    guest_element.click()
                    time.sleep(1)
                    
                    # Попытка установить количество гостей
                    guest_inputs = driver.find_elements(By.CSS_SELECTOR, 'input[type="number"], .guest-count')
                    if guest_inputs:
                        guest_inputs[0].clear()
                        guest_inputs[0].send_keys(str(guests))
                        time.sleep(0.5)
                        
                    # Попытка установить количество комнат
                    room_inputs = driver.find_elements(By.CSS_SELECTOR, '.room-count, .rooms-count')
                    if room_inputs:
                        room_inputs[0].clear()
                        room_inputs[0].send_keys(str(rooms))
                        time.sleep(0.5)
                        
                    break
                except:
                    continue
                    
            return {
                'action': 'configure_guests',
                'guests': guests,
                'rooms': rooms,
                'success': True,
                'timestamp': time.time(),
                'duration': time.time() - start_time
            }
            
        except Exception as e:
            logger.error(f"Ошибка при настройке гостей: {e}")
            return {
                'action': 'configure_guests',
                'guests': guests,
                'rooms': rooms,
                'success': False,
                'error': str(e),
                'timestamp': time.time(),
                'duration': time.time() - start_time
            }
            
    def _search_hotels(self, driver: WebDriver) -> Dict[str, Any]:
        """Поиск отелей"""
        start_time = time.time()
        
        try:
            logger.info("Поиск отелей")
            
            # Поиск кнопки поиска
            search_button_selectors = [
                'button[type="submit"]',
                '.search-button',
                '.find-button',
                '.search-btn'
            ]
            
            search_button = None
            for selector in search_button_selectors:
                try:
                    search_button = driver.find_element(By.CSS_SELECTOR, selector)
                    break
                except:
                    continue
                    
            if search_button:
                search_button.click()
            else:
                # Альтернатива - нажатие Enter в поле поиска
                search_inputs = driver.find_elements(By.CSS_SELECTOR, 'input[name*="query"], input[placeholder*="поиск"]')
                if search_inputs:
                    search_inputs[0].send_keys(Keys.ENTER)
                    
            # Ожидание загрузки результатов
            time.sleep(3)
            
            return {
                'action': 'search_hotels',
                'success': True,
                'timestamp': time.time(),
                'duration': time.time() - start_time
            }
            
        except Exception as e:
            logger.error(f"Ошибка при поиске отелей: {e}")
            return {
                'action': 'search_hotels',
                'success': False,
                'error': str(e),
                'timestamp': time.time(),
                'duration': time.time() - start_time
            }
            
    def _analyze_results(self, driver: WebDriver) -> Dict[str, Any]:
        """Анализ результатов поиска"""
        start_time = time.time()
        
        try:
            logger.info("Анализ результатов поиска")
            
            # Получение HTML страницы
            page_source = driver.page_source
            
            # Подсчет отелей
            hotel_cards = driver.find_elements(By.CSS_SELECTOR, '.hotel-card, .hotel-item, .result-item')
            
            # Анализ фильтров
            filters = driver.find_elements(By.CSS_SELECTOR, '.filter, .facet, .filter-option')
            
            # Анализ сортировки
            sort_options = driver.find_elements(By.CSS_SELECTOR, '.sort, .sort-option, .order-by')
            
            analysis = {
                'hotels_count': len(hotel_cards),
                'filters_count': len(filters),
                'sort_options_count': len(sort_options),
                'page_title': driver.title,
                'current_url': driver.current_url
            }
            
            return {
                'action': 'analyze_results',
                'analysis': analysis,
                'success': True,
                'timestamp': time.time(),
                'duration': time.time() - start_time
            }
            
        except Exception as e:
            logger.error(f"Ошибка при анализе результатов: {e}")
            return {
                'action': 'analyze_results',
                'success': False,
                'error': str(e),
                'timestamp': time.time(),
                'duration': time.time() - start_time
            }
            
    def _analyze_available_filters(self, driver: WebDriver) -> Dict[str, Any]:
        """Анализ доступных фильтров"""
        start_time = time.time()
        
        try:
            logger.info("Анализ доступных фильтров")
            
            filters_analysis = {
                'price_filters': [],
                'star_filters': [],
                'amenity_filters': [],
                'location_filters': []
            }
            
            # Поиск различных типов фильтров
            filter_elements = driver.find_elements(By.CSS_SELECTOR, '.filter, .facet, .filter-option')
            
            for element in filter_elements:
                filter_text = element.text.strip()
                if filter_text:
                    if any(word in filter_text.lower() for word in ['цена', 'стоимость', 'price', 'cost']):
                        filters_analysis['price_filters'].append(filter_text)
                    elif any(word in filter_text.lower() for word in ['звезд', 'star', 'рейтинг']):
                        filters_analysis['star_filters'].append(filter_text)
                    elif any(word in filter_text.lower() for word in ['удобства', 'amenity', 'facility']):
                        filters_analysis['amenity_filters'].append(filter_text)
                    elif any(word in filter_text.lower() for word in ['район', 'location', 'area']):
                        filters_analysis['location_filters'].append(filter_text)
                        
            return {
                'action': 'analyze_available_filters',
                'analysis': filters_analysis,
                'success': True,
                'timestamp': time.time(),
                'duration': time.time() - start_time
            }
            
        except Exception as e:
            logger.error(f"Ошибка при анализе фильтров: {e}")
            return {
                'action': 'analyze_available_filters',
                'success': False,
                'error': str(e),
                'timestamp': time.time(),
                'duration': time.time() - start_time
            }
            
    def _apply_price_filter(self, driver: WebDriver) -> Dict[str, Any]:
        """Применение фильтра по цене"""
        start_time = time.time()
        
        try:
            logger.info("Применение фильтра по цене")
            
            # Поиск фильтра цены
            price_filter_selectors = [
                '.price-filter',
                '.cost-filter',
                '[data-filter="price"]'
            ]
            
            for selector in price_filter_selectors:
                try:
                    price_filter = driver.find_element(By.CSS_SELECTOR, selector)
                    price_filter.click()
                    time.sleep(1)
                    
                    # Попытка установить диапазон цен
                    price_inputs = driver.find_elements(By.CSS_SELECTOR, 'input[type="range"], .price-range input')
                    if price_inputs:
                        # Установка максимальной цены
                        price_inputs[0].send_keys("5000")
                        time.sleep(0.5)
                        
                    break
                except:
                    continue
                    
            return {
                'action': 'apply_price_filter',
                'success': True,
                'timestamp': time.time(),
                'duration': time.time() - start_time
            }
            
        except Exception as e:
            logger.error(f"Ошибка при применении фильтра цены: {e}")
            return {
                'action': 'apply_price_filter',
                'success': False,
                'error': str(e),
                'timestamp': time.time(),
                'duration': time.time() - start_time
            }
            
    def _apply_star_filter(self, driver: WebDriver) -> Dict[str, Any]:
        """Применение фильтра по звездам"""
        start_time = time.time()
        
        try:
            logger.info("Применение фильтра по звездам")
            
            # Поиск фильтра звезд
            star_filter_selectors = [
                '.star-filter',
                '.rating-filter',
                '[data-filter="stars"]'
            ]
            
            for selector in star_filter_selectors:
                try:
                    star_filters = driver.find_elements(By.CSS_SELECTOR, selector)
                    if star_filters:
                        # Выбор 4-5 звезд
                        star_filters[0].click()
                        time.sleep(1)
                        break
                except:
                    continue
                    
            return {
                'action': 'apply_star_filter',
                'success': True,
                'timestamp': time.time(),
                'duration': time.time() - start_time
            }
            
        except Exception as e:
            logger.error(f"Ошибка при применении фильтра звезд: {e}")
            return {
                'action': 'apply_star_filter',
                'success': False,
                'error': str(e),
                'timestamp': time.time(),
                'duration': time.time() - start_time
            }
            
    def _apply_amenity_filter(self, driver: WebDriver) -> Dict[str, Any]:
        """Применение фильтра по удобствам"""
        start_time = time.time()
        
        try:
            logger.info("Применение фильтра по удобствам")
            
            # Поиск фильтра удобств
            amenity_filter_selectors = [
                '.amenity-filter',
                '.facility-filter',
                '[data-filter="amenities"]'
            ]
            
            for selector in amenity_filter_selectors:
                try:
                    amenity_filters = driver.find_elements(By.CSS_SELECTOR, selector)
                    if amenity_filters:
                        # Выбор Wi-Fi
                        for filter in amenity_filters:
                            if 'wi-fi' in filter.text.lower() or 'wifi' in filter.text.lower():
                                filter.click()
                                time.sleep(1)
                                break
                        break
                except:
                    continue
                    
            return {
                'action': 'apply_amenity_filter',
                'success': True,
                'timestamp': time.time(),
                'duration': time.time() - start_time
            }
            
        except Exception as e:
            logger.error(f"Ошибка при применении фильтра удобств: {e}")
            return {
                'action': 'apply_amenity_filter',
                'success': False,
                'error': str(e),
                'timestamp': time.time(),
                'duration': time.time() - start_time
            }
            
    def _analyze_filtered_results(self, driver: WebDriver) -> Dict[str, Any]:
        """Анализ результатов после фильтрации"""
        start_time = time.time()
        
        try:
            logger.info("Анализ результатов после фильтрации")
            
            # Ожидание обновления результатов
            time.sleep(2)
            
            # Подсчет отфильтрованных отелей
            hotel_cards = driver.find_elements(By.CSS_SELECTOR, '.hotel-card, .hotel-item, .result-item')
            
            # Анализ активных фильтров
            active_filters = driver.find_elements(By.CSS_SELECTOR, '.active-filter, .applied-filter')
            
            analysis = {
                'filtered_hotels_count': len(hotel_cards),
                'active_filters_count': len(active_filters),
                'filter_effectiveness': len(hotel_cards) > 0
            }
            
            return {
                'action': 'analyze_filtered_results',
                'analysis': analysis,
                'success': True,
                'timestamp': time.time(),
                'duration': time.time() - start_time
            }
            
        except Exception as e:
            logger.error(f"Ошибка при анализе отфильтрованных результатов: {e}")
            return {
                'action': 'analyze_filtered_results',
                'success': False,
                'error': str(e),
                'timestamp': time.time(),
                'duration': time.time() - start_time
            }
            
    def _select_hotel(self, driver: WebDriver) -> Dict[str, Any]:
        """Выбор отеля"""
        start_time = time.time()
        
        try:
            logger.info("Выбор отеля")
            
            # Поиск карточек отелей
            hotel_cards = driver.find_elements(By.CSS_SELECTOR, '.hotel-card, .hotel-item, .result-item')
            
            if hotel_cards:
                # Клик по первой карточке
                hotel_cards[0].click()
                time.sleep(2)
                
                return {
                    'action': 'select_hotel',
                    'hotel_selected': True,
                    'success': True,
                    'timestamp': time.time(),
                    'duration': time.time() - start_time
                }
            else:
                return {
                    'action': 'select_hotel',
                    'hotel_selected': False,
                    'success': False,
                    'error': 'Отели не найдены',
                    'timestamp': time.time(),
                    'duration': time.time() - start_time
                }
                
        except Exception as e:
            logger.error(f"Ошибка при выборе отеля: {e}")
            return {
                'action': 'select_hotel',
                'success': False,
                'error': str(e),
                'timestamp': time.time(),
                'duration': time.time() - start_time
            }
            
    def _select_room(self, driver: WebDriver) -> Dict[str, Any]:
        """Выбор номера"""
        start_time = time.time()
        
        try:
            logger.info("Выбор номера")
            
            # Поиск кнопок выбора номера
            room_selectors = [
                '.room-select',
                '.book-room',
                '.select-room',
                '.booking-button'
            ]
            
            room_selected = False
            for selector in room_selectors:
                try:
                    room_buttons = driver.find_elements(By.CSS_SELECTOR, selector)
                    if room_buttons:
                        room_buttons[0].click()
                        time.sleep(2)
                        room_selected = True
                        break
                except:
                    continue
                    
            return {
                'action': 'select_room',
                'room_selected': room_selected,
                'success': room_selected,
                'timestamp': time.time(),
                'duration': time.time() - start_time
            }
            
        except Exception as e:
            logger.error(f"Ошибка при выборе номера: {e}")
            return {
                'action': 'select_room',
                'success': False,
                'error': str(e),
                'timestamp': time.time(),
                'duration': time.time() - start_time
            }
            
    def _fill_guest_info(self, driver: WebDriver) -> Dict[str, Any]:
        """Заполнение данных гостей"""
        start_time = time.time()
        
        try:
            logger.info("Заполнение данных гостей")
            
            # Поиск полей формы
            form_fields = driver.find_elements(By.CSS_SELECTOR, 'input[type="text"], input[type="email"]')
            
            if form_fields:
                # Заполнение имени
                if len(form_fields) > 0:
                    form_fields[0].send_keys("Тест Тестов")
                    
                # Заполнение email
                if len(form_fields) > 1:
                    form_fields[1].send_keys("test@example.com")
                    
            return {
                'action': 'fill_guest_info',
                'form_filled': len(form_fields) > 0,
                'success': True,
                'timestamp': time.time(),
                'duration': time.time() - start_time
            }
            
        except Exception as e:
            logger.error(f"Ошибка при заполнении данных гостей: {e}")
            return {
                'action': 'fill_guest_info',
                'success': False,
                'error': str(e),
                'timestamp': time.time(),
                'duration': time.time() - start_time
            }
            
    def _analyze_payment_process(self, driver: WebDriver) -> Dict[str, Any]:
        """Анализ процесса оплаты"""
        start_time = time.time()
        
        try:
            logger.info("Анализ процесса оплаты")
            
            # Поиск элементов оплаты
            payment_elements = driver.find_elements(By.CSS_SELECTOR, '.payment, .payment-method, .payment-option')
            
            # Поиск кнопок оплаты
            payment_buttons = driver.find_elements(By.CSS_SELECTOR, '.pay-button, .payment-button, .checkout-button')
            
            analysis = {
                'payment_methods_count': len(payment_elements),
                'payment_buttons_count': len(payment_buttons),
                'payment_process_available': len(payment_buttons) > 0
            }
            
            return {
                'action': 'analyze_payment_process',
                'analysis': analysis,
                'success': True,
                'timestamp': time.time(),
                'duration': time.time() - start_time
            }
            
        except Exception as e:
            logger.error(f"Ошибка при анализе процесса оплаты: {e}")
            return {
                'action': 'analyze_payment_process',
                'success': False,
                'error': str(e),
                'timestamp': time.time(),
                'duration': time.time() - start_time
            }


