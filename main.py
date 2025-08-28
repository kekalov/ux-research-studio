#!/usr/bin/env python3
"""
AI UX Research Agent для Ostrovok.ru
Основной файл запуска
"""

import argparse
import logging
from datetime import datetime
from pathlib import Path

from agent.ux_agent import UXResearchAgent
from config.settings import load_config
from reports.report_generator import ReportGenerator

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(f'logs/ux_research_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

def main():
    """Основная функция запуска AI агента"""
    
    parser = argparse.ArgumentParser(description='AI UX Research Agent для Ostrovok.ru')
    parser.add_argument('--scenario', 
                       choices=['sochi_winter', 'andorra', 'full_analysis'],
                       default='sochi_winter',
                       help='Сценарий исследования')
    parser.add_argument('--headless', 
                       action='store_true',
                       help='Запуск браузера в фоновом режиме')
    parser.add_argument('--output', 
                       default='reports',
                       help='Папка для сохранения отчетов')
    
    args = parser.parse_args()
    
    # Создание необходимых папок
    Path('logs').mkdir(exist_ok=True)
    Path(args.output).mkdir(exist_ok=True)
    
    # Загрузка конфигурации
    config = load_config()
    
    logger.info(f"Запуск UX исследования: {args.scenario}")
    
    try:
        # Инициализация AI агента
        agent = UXResearchAgent(config, headless=args.headless)
        
        # Выполнение сценария
        results = agent.run_scenario(args.scenario)
        
        # Генерация отчета
        report_gen = ReportGenerator()
        report_path = report_gen.generate_report(results, args.scenario, args.output)
        
        logger.info(f"Исследование завершено. Отчет сохранен: {report_path}")
        
    except Exception as e:
        logger.error(f"Ошибка при выполнении исследования: {e}")
        raise

if __name__ == "__main__":
    main()


