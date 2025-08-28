"""
AI Analyzer - модуль для AI-анализа результатов UX-исследования
"""

import json
import logging
from typing import Dict, Any, List
import openai

logger = logging.getLogger(__name__)

class AIAnalyzer:
    """AI анализатор для UX-исследования"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.client = None
        
        # Инициализация OpenAI клиента
        try:
            import os
            from pathlib import Path
            
            # Загружаем переменные из .env файла
            env_file = Path('.env')
            if env_file.exists():
                with open(env_file, 'r') as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith('#') and '=' in line:
                            key, value = line.split('=', 1)
                            os.environ[key] = value
            
            api_key = os.getenv('OPENAI_API_KEY')
            if api_key:
                self.client = openai.OpenAI(api_key=api_key)
                logger.info("OpenAI клиент инициализирован")
            else:
                logger.warning("OPENAI_API_KEY не найден в переменных окружения")
        except Exception as e:
            logger.error(f"Ошибка при инициализации OpenAI: {e}")
            
    def analyze_results(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Анализ результатов исследования с помощью AI"""
        
        if not self.client:
            logger.warning("OpenAI клиент недоступен, возвращаем базовый анализ")
            return self._basic_analysis(results)
            
        try:
            # Подготовка данных для анализа
            analysis_data = self._prepare_analysis_data(results)
            
            # Создание промпта для AI
            prompt = self._create_analysis_prompt(analysis_data)
            
            # Получение AI анализа
            ai_response = self._get_ai_analysis(prompt)
            
            # Парсинг ответа
            parsed_analysis = self._parse_ai_response(ai_response)
            
            return parsed_analysis
            
        except Exception as e:
            logger.error(f"Ошибка при AI анализе: {e}")
            return self._basic_analysis(results)
            
    def _prepare_analysis_data(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Подготовка данных для анализа"""
        
        analysis_data = {
            'scenario': results.get('scenario', ''),
            'config': results.get('config', {}),
            'steps': results.get('steps', []),
            'successful_steps': len([step for step in results.get('steps', []) if step.get('success', False)]),
            'total_steps': len(results.get('steps', [])),
            'errors': [step.get('error') for step in results.get('steps', []) if step.get('error')],
            'screenshots': results.get('screenshots', [])
        }
        
        # Добавление детальной информации о шагах
        step_details = []
        for step in results.get('steps', []):
            step_detail = {
                'action': step.get('action', ''),
                'success': step.get('success', False),
                'timestamp': step.get('timestamp', 0),
                'duration': step.get('duration', 0)
            }
            
            # Добавление специфичных данных для каждого типа действия
            if step.get('action') == 'search_destination':
                step_detail['destination'] = step.get('destination', '')
            elif step.get('action') == 'select_dates':
                step_detail['check_in'] = step.get('check_in', '')
                step_detail['check_out'] = step.get('check_out', '')
            elif step.get('action') == 'analyze_search_results':
                step_detail['analysis'] = step.get('analysis', {})
                
            step_details.append(step_detail)
            
        analysis_data['step_details'] = step_details
        
        return analysis_data
        
    def _create_analysis_prompt(self, analysis_data: Dict[str, Any]) -> str:
        """Создание промпта для AI анализа"""
        
        scenario = analysis_data['scenario']
        config = analysis_data['config']
        steps = analysis_data['step_details']
        
        prompt = f"""
Ты - опытный UX-аналитик, специализирующийся на анализе пользовательского опыта веб-сайтов бронирования отелей.

Проанализируй результаты автоматизированного UX-исследования сайта Ostrovok.ru.

**Сценарий исследования:** {scenario}
**Описание:** {config.get('description', '')}

**Выполненные шаги:**
"""
        
        for i, step in enumerate(steps, 1):
            prompt += f"""
{i}. {step['action']}
   - Успех: {'Да' if step['success'] else 'Нет'}
   - Время выполнения: {step.get('duration', 0)} сек
"""
            
            if step.get('destination'):
                prompt += f"   - Направление: {step['destination']}\n"
            elif step.get('check_in'):
                prompt += f"   - Даты: {step['check_in']} - {step['check_out']}\n"
            elif step.get('analysis'):
                analysis = step['analysis']
                prompt += f"   - Найдено отелей: {analysis.get('hotels_count', 0)}\n"
                prompt += f"   - Доступно фильтров: {len(analysis.get('filters_available', []))}\n"
                
        prompt += f"""

**Статистика:**
- Успешных шагов: {analysis_data['successful_steps']} из {analysis_data['total_steps']}
- Ошибок: {len(analysis_data['errors'])}

**Задача:** Проведи детальный UX-анализ и предоставь рекомендации по улучшению пользовательского опыта.

**Требования к ответу:**
1. Оценка удобства использования (1-10 баллов)
2. Выявление проблем и узких мест
3. Конкретные рекомендации по улучшению
4. Приоритизация рекомендаций
5. Оценка конкурентоспособности

Ответ предоставь в формате JSON со следующей структурой:
{{
    "overall_score": число от 1 до 10,
    "usability_assessment": {{
        "strengths": ["сильные стороны"],
        "weaknesses": ["слабые стороны"],
        "critical_issues": ["критические проблемы"]
    }},
    "recommendations": [
        {{
            "priority": "high/medium/low",
            "category": "navigation/search/filters/booking/performance",
            "description": "описание рекомендации",
            "impact": "высокий/средний/низкий",
            "effort": "высокий/средний/низкий"
        }}
    ],
    "competitive_analysis": {{
        "score": число от 1 до 10,
        "advantages": ["преимущества"],
        "disadvantages": ["недостатки"]
    }},
    "summary": "краткое резюме анализа"
}}
"""
        
        return prompt
        
    def _get_ai_analysis(self, prompt: str) -> str:
        """Получение анализа от AI"""
        
        try:
            response = self.client.chat.completions.create(
                model=self.config.get('model', 'gpt-4'),
                messages=[
                    {
                        "role": "system",
                        "content": "Ты - опытный UX-аналитик с 10+ летним опытом анализа пользовательского интерфейса. Твоя задача - предоставить детальный, профессиональный анализ пользовательского опыта с конкретными, реализуемыми рекомендациями."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=self.config.get('temperature', 0.7),
                max_tokens=self.config.get('max_tokens', 2000)
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            logger.error(f"Ошибка при получении AI анализа: {e}")
            raise
            
    def _parse_ai_response(self, response: str) -> Dict[str, Any]:
        """Парсинг ответа AI"""
        
        try:
            # Попытка извлечь JSON из ответа
            json_start = response.find('{')
            json_end = response.rfind('}') + 1
            
            if json_start != -1 and json_end != 0:
                json_str = response[json_start:json_end]
                return json.loads(json_str)
            else:
                logger.warning("JSON не найден в ответе AI")
                return self._fallback_analysis(response)
                
        except json.JSONDecodeError as e:
            logger.error(f"Ошибка парсинга JSON: {e}")
            return self._fallback_analysis(response)
            
    def _fallback_analysis(self, response: str) -> Dict[str, Any]:
        """Резервный анализ при ошибке парсинга"""
        
        return {
            "overall_score": 7,
            "usability_assessment": {
                "strengths": ["Базовый функционал работает"],
                "weaknesses": ["Требуется дополнительный анализ"],
                "critical_issues": ["Ошибка в AI анализе"]
            },
            "recommendations": [
                {
                    "priority": "medium",
                    "category": "general",
                    "description": "Провести ручной анализ для уточнения результатов",
                    "impact": "средний",
                    "effort": "средний"
                }
            ],
            "competitive_analysis": {
                "score": 7,
                "advantages": ["Функциональность присутствует"],
                "disadvantages": ["Требуется детальный анализ"]
            },
            "summary": "Требуется дополнительный анализ из-за технических проблем",
            "raw_response": response
        }
        
    def _basic_analysis(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Базовый анализ без AI"""
        
        successful_steps = len([step for step in results.get('steps', []) if step.get('success', False)])
        total_steps = len(results.get('steps', []))
        success_rate = successful_steps / total_steps if total_steps > 0 else 0
        
        # Простая оценка на основе успешности шагов
        if success_rate >= 0.9:
            overall_score = 9
        elif success_rate >= 0.7:
            overall_score = 7
        elif success_rate >= 0.5:
            overall_score = 5
        else:
            overall_score = 3
            
        return {
            "overall_score": overall_score,
            "usability_assessment": {
                "strengths": [
                    f"Успешно выполнено {successful_steps} из {total_steps} шагов",
                    "Базовый функционал работает"
                ],
                "weaknesses": [
                    f"Ошибки в {total_steps - successful_steps} шагах"
                ],
                "critical_issues": []
            },
            "recommendations": [
                {
                    "priority": "medium",
                    "category": "general",
                    "description": "Провести детальный анализ проблемных шагов",
                    "impact": "средний",
                    "effort": "средний"
                }
            ],
            "competitive_analysis": {
                "score": overall_score,
                "advantages": ["Функциональность работает"],
                "disadvantages": ["Требуется улучшение надежности"]
            },
            "summary": f"Базовый анализ: {successful_steps}/{total_steps} шагов выполнено успешно",
            "success_rate": success_rate
        }
        
    def analyze_user_journey(self, steps: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Анализ пользовательского пути"""
        
        if not self.client:
            return self._basic_journey_analysis(steps)
            
        try:
            journey_data = self._prepare_journey_data(steps)
            prompt = self._create_journey_prompt(journey_data)
            ai_response = self._get_ai_analysis(prompt)
            return self._parse_ai_response(ai_response)
            
        except Exception as e:
            logger.error(f"Ошибка при анализе пользовательского пути: {e}")
            return self._basic_journey_analysis(steps)
            
    def _prepare_journey_data(self, steps: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Подготовка данных пользовательского пути"""
        
        journey_data = {
            'total_steps': len(steps),
            'successful_steps': len([step for step in steps if step.get('success', False)]),
            'step_sequence': [],
            'bottlenecks': [],
            'drop_off_points': []
        }
        
        for i, step in enumerate(steps):
            step_info = {
                'step_number': i + 1,
                'action': step.get('action', ''),
                'success': step.get('success', False),
                'duration': step.get('duration', 0),
                'error': step.get('error', '')
            }
            
            journey_data['step_sequence'].append(step_info)
            
            # Выявление узких мест
            if step.get('duration', 0) > 5:  # Шаги дольше 5 секунд
                journey_data['bottlenecks'].append(step_info)
                
            # Выявление точек оттока
            if not step.get('success', False):
                journey_data['drop_off_points'].append(step_info)
                
        return journey_data
        
    def _create_journey_prompt(self, journey_data: Dict[str, Any]) -> str:
        """Создание промпта для анализа пользовательского пути"""
        
        prompt = f"""
Проанализируй пользовательский путь на сайте бронирования отелей.

**Статистика пути:**
- Всего шагов: {journey_data['total_steps']}
- Успешных шагов: {journey_data['successful_steps']}
- Узких мест: {len(journey_data['bottlenecks'])}
- Точек оттока: {len(journey_data['drop_off_points'])}

**Последовательность шагов:**
"""
        
        for step in journey_data['step_sequence']:
            status = "✅" if step['success'] else "❌"
            prompt += f"{status} Шаг {step['step_number']}: {step['action']} ({step['duration']}с)\n"
            
        prompt += f"""

**Узкие места:**
"""
        
        for bottleneck in journey_data['bottlenecks']:
            prompt += f"- Шаг {bottleneck['step_number']}: {bottleneck['action']} ({bottleneck['duration']}с)\n"
            
        prompt += f"""

**Точки оттока:**
"""
        
        for drop_off in journey_data['drop_off_points']:
            prompt += f"- Шаг {drop_off['step_number']}: {drop_off['action']} - {drop_off['error']}\n"
            
        prompt += """

**Задача:** Проанализируй пользовательский путь и предоставь рекомендации по оптимизации.

Ответ в формате JSON:
{
    "journey_score": число от 1 до 10,
    "flow_analysis": {
        "smooth_sections": ["гладкие участки пути"],
        "problematic_sections": ["проблемные участки"],
        "optimization_opportunities": ["возможности оптимизации"]
    },
    "bottleneck_analysis": [
        {
            "step": "номер шага",
            "issue": "описание проблемы",
            "solution": "предлагаемое решение",
            "priority": "high/medium/low"
        }
    ],
    "conversion_optimization": [
        {
            "step": "номер шага",
            "optimization": "описание оптимизации",
            "expected_impact": "ожидаемый эффект"
        }
    ],
    "summary": "краткое резюме анализа пути"
}
"""
        
        return prompt
        
    def _basic_journey_analysis(self, steps: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Базовый анализ пользовательского пути"""
        
        successful_steps = len([step for step in steps if step.get('success', False)])
        total_steps = len(steps)
        success_rate = successful_steps / total_steps if total_steps > 0 else 0
        
        bottlenecks = [step for step in steps if step.get('duration', 0) > 5]
        drop_offs = [step for step in steps if not step.get('success', False)]
        
        return {
            "journey_score": int(success_rate * 10),
            "flow_analysis": {
                "smooth_sections": [f"Шаги 1-{successful_steps}"],
                "problematic_sections": [f"Шаги {successful_steps + 1}-{total_steps}"],
                "optimization_opportunities": ["Улучшение надежности шагов"]
            },
            "bottleneck_analysis": [
                {
                    "step": step.get('action', ''),
                    "issue": f"Длительное выполнение ({step.get('duration', 0)}с)",
                    "solution": "Оптимизация производительности",
                    "priority": "medium"
                }
                for step in bottlenecks
            ],
            "conversion_optimization": [
                {
                    "step": step.get('action', ''),
                    "optimization": "Исправление ошибок",
                    "expected_impact": "Повышение успешности"
                }
                for step in drop_offs
            ],
            "summary": f"Путь: {successful_steps}/{total_steps} шагов успешно, {len(bottlenecks)} узких мест, {len(drop_offs)} точек оттока"
        }
