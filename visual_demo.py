"""
Visual Demo - визуальная демонстрация выполнения задания агентом
"""

import time
import random
import json
from datetime import datetime
from pathlib import Path

def create_visual_demo():
    """Создание визуальной демонстрации"""
    
    print("🎭 ВИЗУАЛЬНАЯ ДЕМОНСТРАЦИЯ AI UX AGENT")
    print("=" * 60)
    print("Симуляция реального пользователя на сайте Ostrovok.ru")
    print("=" * 60)
    
    # Сценарий: поиск отеля в Сочи на зимний сезон
    scenario = {
        'destination': 'Сочи',
        'dates': '20-27 декабря 2024',
        'guests': '2 взрослых, 1 комната',
        'goal': 'Найти и забронировать отель для зимнего отдыха'
    }
    
    print(f"\n🎯 ЦЕЛЬ: {scenario['goal']}")
    print(f"📍 Направление: {scenario['destination']}")
    print(f"📅 Даты: {scenario['dates']}")
    print(f"👥 Гости: {scenario['guests']}")
    
    # Шаги выполнения с визуализацией
    steps = [
        {
            'action': 'Открытие сайта',
            'description': 'Переход на ostrovok.ru',
            'duration': 3,
            'thoughts': 'Открываю главную страницу сайта...',
            'status': 'success'
        },
        {
            'action': 'Изучение интерфейса',
            'description': 'Поиск поля ввода направления',
            'duration': 4,
            'thoughts': 'Ищу поле поиска... Нашел!',
            'status': 'success'
        },
        {
            'action': 'Ввод направления',
            'description': 'Печать "Сочи" в поле поиска',
            'duration': 2,
            'thoughts': 'Печатаю медленно: С-О-Ч-И...',
            'status': 'success'
        },
        {
            'action': 'Выбор дат',
            'description': 'Открытие календаря и выбор дат',
            'duration': 6,
            'thoughts': 'Открываю календарь, выбираю 20-27 декабря...',
            'status': 'success'
        },
        {
            'action': 'Настройка гостей',
            'description': 'Указание количества гостей и комнат',
            'duration': 3,
            'thoughts': '2 взрослых, 1 комната - готово!',
            'status': 'success'
        },
        {
            'action': 'Запуск поиска',
            'description': 'Нажатие кнопки "Найти"',
            'duration': 1,
            'thoughts': 'Нажимаю поиск, жду результаты...',
            'status': 'success'
        },
        {
            'action': 'Ожидание результатов',
            'description': 'Загрузка списка отелей',
            'duration': 5,
            'thoughts': 'Загружаются результаты поиска...',
            'status': 'success'
        },
        {
            'action': 'Анализ результатов',
            'description': 'Просмотр найденных отелей',
            'duration': 8,
            'thoughts': 'Отлично! 47 отелей найдено. Смотрю варианты...',
            'status': 'success'
        },
        {
            'action': 'Применение фильтров',
            'description': 'Фильтрация по цене и звездам',
            'duration': 4,
            'thoughts': 'Применяю фильтр по цене до 10000 рублей...',
            'status': 'success'
        },
        {
            'action': 'Проблема с фильтром',
            'description': 'Фильтр по звездам не работает',
            'duration': 7,
            'thoughts': 'Почему фильтр по звездам не работает? Попробую другой...',
            'status': 'error'
        },
        {
            'action': 'Выбор отеля',
            'description': 'Клик по понравившемуся отелю',
            'duration': 3,
            'thoughts': 'Этот отель выглядит хорошо, кликаю...',
            'status': 'success'
        },
        {
            'action': 'Просмотр деталей',
            'description': 'Изучение информации об отеле',
            'duration': 6,
            'thoughts': 'Смотрю фото, читаю отзывы, проверяю цены...',
            'status': 'success'
        },
        {
            'action': 'Проверка доступности',
            'description': 'Проверка свободных номеров',
            'duration': 4,
            'thoughts': 'Проверяю, есть ли свободные номера на мои даты...',
            'status': 'success'
        },
        {
            'action': 'Выбор тарифа',
            'description': 'Выбор типа номера и условий',
            'duration': 5,
            'thoughts': 'Выбираю стандартный номер с завтраком...',
            'status': 'success'
        }
    ]
    
    print(f"\n🚀 НАЧИНАЕМ ВЫПОЛНЕНИЕ ЗАДАНИЯ...")
    print(f"Всего шагов: {len(steps)}")
    
    total_time = 0
    successful_steps = 0
    failed_steps = 0
    
    for i, step in enumerate(steps, 1):
        print(f"\n📋 ШАГ {i}/{len(steps)}: {step['action']}")
        print(f"   📝 {step['description']}")
        print(f"   💭 \"{step['thoughts']}\"")
        
        # Анимация выполнения
        duration = step['duration']
        total_time += duration
        
        print(f"   ⏱️  Выполнение: ", end="", flush=True)
        for _ in range(duration):
            print("█", end="", flush=True)
            time.sleep(0.2)
        print()
        
        # Результат шага
        if step['status'] == 'success':
            print(f"   ✅ УСПЕШНО ({duration} сек)")
            successful_steps += 1
        else:
            print(f"   ❌ ОШИБКА ({duration} сек)")
            failed_steps += 1
            print(f"   🔧 Проблема: {step['description']}")
    
    # Итоговая статистика
    print(f"\n" + "=" * 60)
    print(f"🎉 ЗАДАНИЕ ВЫПОЛНЕНО!")
    print(f"=" * 60)
    print(f"⏱️  Общее время: {total_time} секунд ({total_time/60:.1f} минут)")
    print(f"✅ Успешных шагов: {successful_steps}/{len(steps)}")
    print(f"❌ Ошибок: {failed_steps}")
    print(f"📊 Успешность: {successful_steps/len(steps)*100:.1f}%")
    
    # Оценка опыта
    if successful_steps/len(steps) >= 0.9:
        rating = 9
        experience = "Отличный"
    elif successful_steps/len(steps) >= 0.8:
        rating = 8
        experience = "Хороший"
    elif successful_steps/len(steps) >= 0.7:
        rating = 7
        experience = "Удовлетворительный"
    else:
        rating = 5
        experience = "Плохой"
    
    print(f"⭐ Оценка опыта: {rating}/10 ({experience})")
    
    # Фидбэк от пользователя
    print(f"\n👤 ФИДБЭК ОТ ПОЛЬЗОВАТЕЛЯ:")
    print(f"   \"{experience} опыт! Смог найти подходящий отель в Сочи.")
    if failed_steps > 0:
        print(f"   Единственная проблема - фильтр по звездам работал нестабильно.")
    print(f"   Общее впечатление положительное, рекомендую сайт.\"")
    
    # Рекомендации
    print(f"\n💡 РЕКОМЕНДАЦИИ ДЛЯ УЛУЧШЕНИЯ:")
    if failed_steps > 0:
        print(f"   🔧 Исправить работу фильтров")
    if total_time > 60:
        print(f"   ⚡ Оптимизировать скорость загрузки")
    print(f"   🎨 Улучшить визуальное оформление")
    print(f"   📱 Добавить мобильную версию")
    
    return {
        'scenario': scenario,
        'steps': steps,
        'total_time': total_time,
        'success_rate': successful_steps/len(steps),
        'rating': rating,
        'experience': experience
    }

def create_screenshot_demo():
    """Создание демонстрации со скриншотами (концепт)"""
    
    print(f"\n📸 КОНЦЕПТ ДЕМОНСТРАЦИИ СО СКРИНШОТАМИ:")
    print(f"   В реальной версии агент мог бы:")
    print(f"   📱 Делать скриншоты каждого шага")
    print(f"   🎬 Создавать видео-запись процесса")
    print(f"   📊 Показывать тепловые карты кликов")
    print(f"   🎯 Отмечать проблемные области")
    print(f"   📈 Анализировать время на каждом элементе")

if __name__ == "__main__":
    result = create_visual_demo()
    create_screenshot_demo()
    
    print(f"\n🎭 Демонстрация завершена!")
    print(f"💡 Теперь вы видели, как агент выполняет задание пошагово!")


