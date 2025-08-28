# Инструкции по установке AI UX Research Agent

## Требования

- Python 3.8+
- Chrome браузер
- OpenAI API ключ (опционально, для AI анализа)

## Установка

### 1. Клонирование репозитория

```bash
git clone <repository-url>
cd ost-agent
```

### 2. Установка зависимостей

```bash
pip install -r requirements.txt
```

### 3. Установка Chrome WebDriver

WebDriver будет автоматически установлен при первом запуске благодаря `webdriver-manager`.

### 4. Настройка OpenAI API (опционально)

Для полного AI анализа установите переменную окружения:

```bash
export OPENAI_API_KEY='your-openai-api-key-here'
```

Или добавьте в файл `.env`:

```
OPENAI_API_KEY=your-openai-api-key-here
```

## Использование

### Базовое использование

```bash
# Запуск сценария поиска отелей в Сочи
python main.py --scenario sochi_winter

# Запуск сценария поиска отелей в Андорре
python main.py --scenario andorra

# Полный анализ всех функций
python main.py --scenario full_analysis
```

### Дополнительные опции

```bash
# Запуск в фоновом режиме (без открытия браузера)
python main.py --scenario sochi_winter --headless

# Указание папки для отчетов
python main.py --scenario sochi_winter --output custom_reports
```

### Пример использования

```bash
# Запуск примера
python examples/example_usage.py
```

## Структура проекта

```
ost-agent/
├── main.py                 # Основной файл запуска
├── requirements.txt        # Зависимости
├── README.md              # Документация
├── INSTALL.md             # Инструкции по установке
├── config/                # Конфигурация
│   ├── __init__.py
│   └── settings.py
├── agent/                 # AI агент
│   ├── __init__.py
│   ├── ux_agent.py        # Основной класс агента
│   ├── web_analyzer.py    # Анализатор веб-страниц
│   ├── ai_analyzer.py     # AI анализатор
│   └── scenario_executor.py # Исполнитель сценариев
├── reports/               # Генератор отчетов
│   ├── __init__.py
│   └── report_generator.py
├── examples/              # Примеры использования
│   └── example_usage.py
├── logs/                  # Логи (создается автоматически)
└── reports/               # Отчеты (создается автоматически)
```

## Сценарии исследования

### 1. sochi_winter
- **Описание**: Поиск отелей в Сочи на зимний сезон
- **Даты**: 20-27 декабря 2024
- **Гости**: 2 человека, 1 комната
- **Анализ**: Поиск, фильтрация, анализ результатов

### 2. andorra
- **Описание**: Поиск отелей в Андорре для горнолыжного отдыха
- **Даты**: 25 декабря 2024 - 2 января 2025
- **Гости**: 2 человека, 1 комната
- **Анализ**: Поиск, фильтрация, анализ результатов

### 3. full_analysis
- **Описание**: Полный анализ всех функций сайта
- **Анализ**: Главная страница, поиск, фильтры, процесс бронирования

## Настройка

### Конфигурация сценариев

Отредактируйте файл `config/settings.py` для изменения:

- Дат поездок
- Количества гостей
- Направлений
- Селекторов элементов

### Добавление новых сценариев

1. Добавьте новый сценарий в `config/settings.py`
2. Реализуйте логику в `agent/ux_agent.py`
3. Обновите `main.py` для поддержки нового сценария

## Отчеты

После выполнения исследования генерируются:

- **HTML отчет**: Детальный анализ с визуализацией
- **JSON отчет**: Структурированные данные
- **Графики**: Диаграммы производительности
- **Скриншоты**: Изображения страниц

## Устранение неполадок

### Проблемы с WebDriver

```bash
# Очистка кэша WebDriver
rm -rf ~/.wdm/
```

### Проблемы с Chrome

```bash
# Обновление Chrome
# На macOS:
brew install --cask google-chrome

# На Ubuntu:
sudo apt update && sudo apt install google-chrome-stable
```

### Проблемы с зависимостями

```bash
# Обновление pip
pip install --upgrade pip

# Переустановка зависимостей
pip uninstall -r requirements.txt
pip install -r requirements.txt
```

## Поддержка

При возникновении проблем:

1. Проверьте логи в папке `logs/`
2. Убедитесь в актуальности Chrome браузера
3. Проверьте подключение к интернету
4. Убедитесь в корректности OpenAI API ключа

## Лицензия

MIT License


