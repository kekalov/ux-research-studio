"""
Web Analyzer - модуль для анализа веб-страниц и элементов
"""

import re
import logging
from typing import Dict, Any, List
from bs4 import BeautifulSoup
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By

logger = logging.getLogger(__name__)

class WebAnalyzer:
    """Анализатор веб-страниц"""
    
    def __init__(self):
        self.soup = None
        
    def analyze_homepage(self, html_content: str) -> Dict[str, Any]:
        """Анализ главной страницы"""
        logger.info("Анализ главной страницы")
        
        self.soup = BeautifulSoup(html_content, 'html.parser')
        
        analysis = {
            'page_title': self._get_page_title(),
            'search_elements': self._analyze_search_elements(),
            'navigation': self._analyze_navigation(),
            'content_sections': self._analyze_content_sections(),
            'performance_indicators': self._analyze_performance_indicators(),
            'accessibility': self._analyze_accessibility()
        }
        
        return analysis
        
    def analyze_search_results(self, html_content: str) -> Dict[str, Any]:
        """Анализ результатов поиска"""
        logger.info("Анализ результатов поиска")
        
        self.soup = BeautifulSoup(html_content, 'html.parser')
        
        analysis = {
            'hotels_count': self._count_hotels(),
            'filters_available': self._analyze_available_filters(),
            'sorting_options': self._analyze_sorting_options(),
            'hotel_cards': self._analyze_hotel_cards(),
            'pagination': self._analyze_pagination(),
            'price_range': self._analyze_price_range()
        }
        
        return analysis
        
    def analyze_search_elements(self, driver: WebDriver) -> Dict[str, Any]:
        """Анализ элементов поиска"""
        logger.info("Анализ элементов поиска")
        
        analysis = {
            'search_box': self._analyze_search_box(driver),
            'date_pickers': self._analyze_date_pickers(driver),
            'guest_selectors': self._analyze_guest_selectors(driver),
            'search_button': self._analyze_search_button(driver)
        }
        
        return analysis
        
    def analyze_filters(self, driver: WebDriver) -> Dict[str, Any]:
        """Анализ фильтров"""
        logger.info("Анализ фильтров")
        
        analysis = {
            'price_filters': self._analyze_price_filters(driver),
            'star_rating_filters': self._analyze_star_filters(driver),
            'amenity_filters': self._analyze_amenity_filters(driver),
            'location_filters': self._analyze_location_filters(driver)
        }
        
        return analysis
        
    def analyze_booking_process(self, driver: WebDriver) -> Dict[str, Any]:
        """Анализ процесса бронирования"""
        logger.info("Анализ процесса бронирования")
        
        analysis = {
            'booking_buttons': self._analyze_booking_buttons(driver),
            'room_selection': self._analyze_room_selection(driver),
            'guest_info_form': self._analyze_guest_form(driver),
            'payment_options': self._analyze_payment_options(driver)
        }
        
        return analysis
        
    def _get_page_title(self) -> str:
        """Получение заголовка страницы"""
        title = self.soup.find('title')
        return title.get_text().strip() if title else "Заголовок не найден"
        
    def _analyze_search_elements(self) -> Dict[str, Any]:
        """Анализ элементов поиска на главной странице"""
        search_elements = {
            'search_box': self._find_search_box(),
            'destination_suggestions': self._find_destination_suggestions(),
            'date_inputs': self._find_date_inputs(),
            'guest_inputs': self._find_guest_inputs()
        }
        
        return search_elements
        
    def _analyze_navigation(self) -> Dict[str, Any]:
        """Анализ навигации"""
        navigation = {
            'main_menu': self._find_main_menu(),
            'breadcrumbs': self._find_breadcrumbs(),
            'footer_links': self._find_footer_links()
        }
        
        return navigation
        
    def _analyze_content_sections(self) -> Dict[str, Any]:
        """Анализ основных секций контента"""
        sections = {
            'hero_section': self._find_hero_section(),
            'featured_destinations': self._find_featured_destinations(),
            'special_offers': self._find_special_offers(),
            'testimonials': self._find_testimonials()
        }
        
        return sections
        
    def _analyze_performance_indicators(self) -> Dict[str, Any]:
        """Анализ индикаторов производительности"""
        indicators = {
            'load_time': None,  # Будет заполнено из метрик
            'images_count': len(self.soup.find_all('img')),
            'scripts_count': len(self.soup.find_all('script')),
            'css_files_count': len(self.soup.find_all('link', rel='stylesheet'))
        }
        
        return indicators
        
    def _analyze_accessibility(self) -> Dict[str, Any]:
        """Анализ доступности"""
        accessibility = {
            'alt_texts': self._check_alt_texts(),
            'aria_labels': self._check_aria_labels(),
            'semantic_elements': self._check_semantic_elements()
        }
        
        return accessibility
        
    def _count_hotels(self) -> int:
        """Подсчет количества отелей в результатах"""
        hotel_cards = self.soup.find_all(class_=re.compile(r'hotel|card|item'))
        return len(hotel_cards)
        
    def _analyze_available_filters(self) -> List[str]:
        """Анализ доступных фильтров"""
        filters = []
        
        # Поиск различных типов фильтров
        filter_elements = self.soup.find_all(class_=re.compile(r'filter|facet'))
        
        for element in filter_elements:
            filter_text = element.get_text().strip()
            if filter_text:
                filters.append(filter_text)
                
        return filters
        
    def _analyze_sorting_options(self) -> List[str]:
        """Анализ опций сортировки"""
        sorting_options = []
        
        sort_elements = self.soup.find_all(class_=re.compile(r'sort|order'))
        
        for element in sort_elements:
            option_text = element.get_text().strip()
            if option_text:
                sorting_options.append(option_text)
                
        return sorting_options
        
    def _analyze_hotel_cards(self) -> Dict[str, Any]:
        """Анализ карточек отелей"""
        cards_analysis = {
            'total_cards': 0,
            'cards_with_images': 0,
            'cards_with_prices': 0,
            'cards_with_ratings': 0,
            'average_price': 0
        }
        
        hotel_cards = self.soup.find_all(class_=re.compile(r'hotel|card'))
        cards_analysis['total_cards'] = len(hotel_cards)
        
        prices = []
        for card in hotel_cards:
            # Проверка наличия изображений
            if card.find('img'):
                cards_analysis['cards_with_images'] += 1
                
            # Проверка наличия цен
            price_element = card.find(class_=re.compile(r'price|cost'))
            if price_element:
                cards_analysis['cards_with_prices'] += 1
                price_text = price_element.get_text()
                price_match = re.search(r'\d+', price_text.replace(' ', ''))
                if price_match:
                    prices.append(int(price_match.group()))
                    
            # Проверка наличия рейтингов
            rating_element = card.find(class_=re.compile(r'rating|star'))
            if rating_element:
                cards_analysis['cards_with_ratings'] += 1
                
        if prices:
            cards_analysis['average_price'] = sum(prices) / len(prices)
            
        return cards_analysis
        
    def _analyze_pagination(self) -> Dict[str, Any]:
        """Анализ пагинации"""
        pagination = {
            'has_pagination': False,
            'current_page': 1,
            'total_pages': 1,
            'next_page_available': False
        }
        
        pagination_element = self.soup.find(class_=re.compile(r'pagination|pages'))
        if pagination_element:
            pagination['has_pagination'] = True
            
            # Поиск текущей страницы
            current_page = pagination_element.find(class_=re.compile(r'current|active'))
            if current_page:
                page_text = current_page.get_text()
                page_match = re.search(r'\d+', page_text)
                if page_match:
                    pagination['current_page'] = int(page_match.group())
                    
            # Поиск кнопки следующей страницы
            next_button = pagination_element.find(class_=re.compile(r'next|forward'))
            if next_button and not 'disabled' in next_button.get('class', []):
                pagination['next_page_available'] = True
                
        return pagination
        
    def _analyze_price_range(self) -> Dict[str, Any]:
        """Анализ диапазона цен"""
        price_range = {
            'min_price': None,
            'max_price': None,
            'price_distribution': {}
        }
        
        price_elements = self.soup.find_all(class_=re.compile(r'price|cost'))
        prices = []
        
        for element in price_elements:
            price_text = element.get_text()
            price_match = re.search(r'\d+', price_text.replace(' ', ''))
            if price_match:
                price = int(price_match.group())
                prices.append(price)
                
        if prices:
            price_range['min_price'] = min(prices)
            price_range['max_price'] = max(prices)
            
            # Распределение цен по диапазонам
            if price_range['max_price'] > price_range['min_price']:
                range_size = (price_range['max_price'] - price_range['min_price']) / 5
                for i in range(5):
                    start = price_range['min_price'] + i * range_size
                    end = price_range['min_price'] + (i + 1) * range_size
                    count = len([p for p in prices if start <= p < end])
                    price_range['price_distribution'][f'{int(start)}-{int(end)}'] = count
                    
        return price_range
        
    def _find_search_box(self) -> Dict[str, Any]:
        """Поиск поля поиска"""
        search_box = self.soup.find('input', attrs={'name': re.compile(r'query|search|destination')})
        
        if search_box:
            return {
                'found': True,
                'placeholder': search_box.get('placeholder', ''),
                'type': search_box.get('type', 'text'),
                'required': search_box.get('required') is not None
            }
        else:
            return {'found': False}
            
    def _find_destination_suggestions(self) -> List[str]:
        """Поиск предложений направлений"""
        suggestions = []
        
        # Поиск элементов с предложениями
        suggestion_elements = self.soup.find_all(class_=re.compile(r'suggestion|autocomplete|dropdown'))
        
        for element in suggestion_elements:
            suggestion_text = element.get_text().strip()
            if suggestion_text:
                suggestions.append(suggestion_text)
                
        return suggestions
        
    def _find_date_inputs(self) -> List[Dict[str, Any]]:
        """Поиск полей ввода дат"""
        date_inputs = []
        
        # Поиск полей дат
        date_elements = self.soup.find_all('input', attrs={'type': 'date'})
        date_elements.extend(self.soup.find_all(class_=re.compile(r'date|calendar')))
        
        for element in date_elements:
            date_inputs.append({
                'type': element.get('type', 'text'),
                'placeholder': element.get('placeholder', ''),
                'required': element.get('required') is not None
            })
            
        return date_inputs
        
    def _find_guest_inputs(self) -> List[Dict[str, Any]]:
        """Поиск полей для ввода количества гостей"""
        guest_inputs = []
        
        # Поиск элементов для гостей
        guest_elements = self.soup.find_all(class_=re.compile(r'guest|person|traveler'))
        
        for element in guest_elements:
            guest_inputs.append({
                'text': element.get_text().strip(),
                'type': element.get('type', 'text')
            })
            
        return guest_inputs
        
    def _find_main_menu(self) -> List[str]:
        """Поиск главного меню"""
        menu_items = []
        
        # Поиск элементов меню
        menu_elements = self.soup.find_all(class_=re.compile(r'menu|nav|header'))
        
        for element in menu_elements:
            links = element.find_all('a')
            for link in links:
                link_text = link.get_text().strip()
                if link_text:
                    menu_items.append(link_text)
                    
        return menu_items
        
    def _find_breadcrumbs(self) -> List[str]:
        """Поиск хлебных крошек"""
        breadcrumbs = []
        
        # Поиск хлебных крошек
        breadcrumb_elements = self.soup.find_all(class_=re.compile(r'breadcrumb|bread'))
        
        for element in breadcrumb_elements:
            links = element.find_all('a')
            for link in links:
                link_text = link.get_text().strip()
                if link_text:
                    breadcrumbs.append(link_text)
                    
        return breadcrumbs
        
    def _find_footer_links(self) -> List[str]:
        """Поиск ссылок в футере"""
        footer_links = []
        
        # Поиск футера
        footer = self.soup.find('footer')
        if footer:
            links = footer.find_all('a')
            for link in links:
                link_text = link.get_text().strip()
                if link_text:
                    footer_links.append(link_text)
                    
        return footer_links
        
    def _find_hero_section(self) -> Dict[str, Any]:
        """Поиск главной секции"""
        hero = {
            'found': False,
            'title': '',
            'subtitle': '',
            'cta_button': ''
        }
        
        # Поиск главной секции
        hero_element = self.soup.find(class_=re.compile(r'hero|banner|main'))
        
        if hero_element:
            hero['found'] = True
            
            # Поиск заголовка
            title = hero_element.find(['h1', 'h2'])
            if title:
                hero['title'] = title.get_text().strip()
                
            # Поиск подзаголовка
            subtitle = hero_element.find(['h3', 'h4', 'p'])
            if subtitle:
                hero['subtitle'] = subtitle.get_text().strip()
                
            # Поиск кнопки призыва к действию
            cta_button = hero_element.find('button')
            if cta_button:
                hero['cta_button'] = cta_button.get_text().strip()
                
        return hero
        
    def _find_featured_destinations(self) -> List[str]:
        """Поиск популярных направлений"""
        destinations = []
        
        # Поиск секции с направлениями
        destinations_section = self.soup.find(class_=re.compile(r'destination|popular|featured'))
        
        if destinations_section:
            destination_elements = destinations_section.find_all(class_=re.compile(r'city|destination|place'))
            
            for element in destination_elements:
                destination_text = element.get_text().strip()
                if destination_text:
                    destinations.append(destination_text)
                    
        return destinations
        
    def _find_special_offers(self) -> List[str]:
        """Поиск специальных предложений"""
        offers = []
        
        # Поиск секции с предложениями
        offers_section = self.soup.find(class_=re.compile(r'offer|deal|promotion'))
        
        if offers_section:
            offer_elements = offers_section.find_all(class_=re.compile(r'offer|deal'))
            
            for element in offer_elements:
                offer_text = element.get_text().strip()
                if offer_text:
                    offers.append(offer_text)
                    
        return offers
        
    def _find_testimonials(self) -> List[str]:
        """Поиск отзывов"""
        testimonials = []
        
        # Поиск секции с отзывами
        testimonials_section = self.soup.find(class_=re.compile(r'testimonial|review|feedback'))
        
        if testimonials_section:
            testimonial_elements = testimonials_section.find_all(class_=re.compile(r'testimonial|review'))
            
            for element in testimonial_elements:
                testimonial_text = element.get_text().strip()
                if testimonial_text:
                    testimonials.append(testimonial_text)
                    
        return testimonials
        
    def _check_alt_texts(self) -> Dict[str, Any]:
        """Проверка alt-текстов изображений"""
        images = self.soup.find_all('img')
        total_images = len(images)
        images_with_alt = len([img for img in images if img.get('alt')])
        
        return {
            'total_images': total_images,
            'images_with_alt': images_with_alt,
            'alt_coverage': images_with_alt / total_images if total_images > 0 else 0
        }
        
    def _check_aria_labels(self) -> Dict[str, Any]:
        """Проверка aria-лейблов"""
        elements_with_aria = self.soup.find_all(attrs={'aria-label': True})
        
        return {
            'elements_with_aria': len(elements_with_aria),
            'aria_labels': [elem.get('aria-label') for elem in elements_with_aria]
        }
        
    def _check_semantic_elements(self) -> Dict[str, Any]:
        """Проверка семантических элементов"""
        semantic_elements = {
            'header': len(self.soup.find_all('header')),
            'nav': len(self.soup.find_all('nav')),
            'main': len(self.soup.find_all('main')),
            'section': len(self.soup.find_all('section')),
            'article': len(self.soup.find_all('article')),
            'aside': len(self.soup.find_all('aside')),
            'footer': len(self.soup.find_all('footer'))
        }
        
        return semantic_elements
        
    # Методы для анализа с помощью Selenium
    def _analyze_search_box(self, driver: WebDriver) -> Dict[str, Any]:
        """Анализ поля поиска с помощью Selenium"""
        try:
            search_box = driver.find_element(By.CSS_SELECTOR, 'input[name*="query"], input[placeholder*="поиск"]')
            return {
                'found': True,
                'placeholder': search_box.get_attribute('placeholder'),
                'type': search_box.get_attribute('type'),
                'enabled': search_box.is_enabled(),
                'displayed': search_box.is_displayed()
            }
        except:
            return {'found': False}
            
    def _analyze_date_pickers(self, driver: WebDriver) -> Dict[str, Any]:
        """Анализ выбора дат"""
        try:
            date_elements = driver.find_elements(By.CSS_SELECTOR, 'input[type="date"], .date-picker')
            return {
                'count': len(date_elements),
                'elements': [{'type': elem.get_attribute('type'), 'enabled': elem.is_enabled()} for elem in date_elements]
            }
        except:
            return {'count': 0, 'elements': []}
            
    def _analyze_guest_selectors(self, driver: WebDriver) -> Dict[str, Any]:
        """Анализ селекторов гостей"""
        try:
            guest_elements = driver.find_elements(By.CSS_SELECTOR, '.guest-selector, .traveler-selector')
            return {
                'count': len(guest_elements),
                'elements': [{'text': elem.text, 'enabled': elem.is_enabled()} for elem in guest_elements]
            }
        except:
            return {'count': 0, 'elements': []}
            
    def _analyze_search_button(self, driver: WebDriver) -> Dict[str, Any]:
        """Анализ кнопки поиска"""
        try:
            search_button = driver.find_element(By.CSS_SELECTOR, 'button[type="submit"], .search-button')
            return {
                'found': True,
                'text': search_button.text,
                'enabled': search_button.is_enabled(),
                'displayed': search_button.is_displayed()
            }
        except:
            return {'found': False}
            
    def _analyze_price_filters(self, driver: WebDriver) -> Dict[str, Any]:
        """Анализ фильтров цен"""
        try:
            price_filters = driver.find_elements(By.CSS_SELECTOR, '.price-filter, .cost-filter')
            return {
                'count': len(price_filters),
                'filters': [{'text': elem.text, 'enabled': elem.is_enabled()} for elem in price_filters]
            }
        except:
            return {'count': 0, 'filters': []}
            
    def _analyze_star_filters(self, driver: WebDriver) -> Dict[str, Any]:
        """Анализ фильтров по звездам"""
        try:
            star_filters = driver.find_elements(By.CSS_SELECTOR, '.star-filter, .rating-filter')
            return {
                'count': len(star_filters),
                'filters': [{'text': elem.text, 'enabled': elem.is_enabled()} for elem in star_filters]
            }
        except:
            return {'count': 0, 'filters': []}
            
    def _analyze_amenity_filters(self, driver: WebDriver) -> Dict[str, Any]:
        """Анализ фильтров удобств"""
        try:
            amenity_filters = driver.find_elements(By.CSS_SELECTOR, '.amenity-filter, .facility-filter')
            return {
                'count': len(amenity_filters),
                'filters': [{'text': elem.text, 'enabled': elem.is_enabled()} for elem in amenity_filters]
            }
        except:
            return {'count': 0, 'filters': []}
            
    def _analyze_location_filters(self, driver: WebDriver) -> Dict[str, Any]:
        """Анализ фильтров местоположения"""
        try:
            location_filters = driver.find_elements(By.CSS_SELECTOR, '.location-filter, .area-filter')
            return {
                'count': len(location_filters),
                'filters': [{'text': elem.text, 'enabled': elem.is_enabled()} for elem in location_filters]
            }
        except:
            return {'count': 0, 'filters': []}
            
    def _analyze_booking_buttons(self, driver: WebDriver) -> Dict[str, Any]:
        """Анализ кнопок бронирования"""
        try:
            booking_buttons = driver.find_elements(By.CSS_SELECTOR, '.booking-button, .book-button')
            return {
                'count': len(booking_buttons),
                'buttons': [{'text': elem.text, 'enabled': elem.is_enabled()} for elem in booking_buttons]
            }
        except:
            return {'count': 0, 'buttons': []}
            
    def _analyze_room_selection(self, driver: WebDriver) -> Dict[str, Any]:
        """Анализ выбора комнат"""
        try:
            room_elements = driver.find_elements(By.CSS_SELECTOR, '.room-selection, .room-option')
            return {
                'count': len(room_elements),
                'options': [{'text': elem.text, 'enabled': elem.is_enabled()} for elem in room_elements]
            }
        except:
            return {'count': 0, 'options': []}
            
    def _analyze_guest_form(self, driver: WebDriver) -> Dict[str, Any]:
        """Анализ формы гостей"""
        try:
            form_elements = driver.find_elements(By.CSS_SELECTOR, '.guest-form, .traveler-form')
            return {
                'count': len(form_elements),
                'forms': [{'text': elem.text, 'enabled': elem.is_enabled()} for elem in form_elements]
            }
        except:
            return {'count': 0, 'forms': []}
            
    def _analyze_payment_options(self, driver: WebDriver) -> Dict[str, Any]:
        """Анализ опций оплаты"""
        try:
            payment_elements = driver.find_elements(By.CSS_SELECTOR, '.payment-option, .payment-method')
            return {
                'count': len(payment_elements),
                'options': [{'text': elem.text, 'enabled': elem.is_enabled()} for elem in payment_elements]
            }
        except:
            return {'count': 0, 'options': []}


