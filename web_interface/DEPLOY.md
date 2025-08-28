# 🚀 Деплой UX Research Studio на Render

## 📋 Подготовка к деплою

### 1. Подготовка репозитория
```bash
# Убедитесь, что все файлы в папке web_interface
cd web_interface
git add .
git commit -m "Add web interface for UX Research Studio"
git push origin main
```

### 2. Настройка Render

#### Шаг 1: Создание нового Web Service
1. Зайдите на [render.com](https://render.com)
2. Нажмите "New +" → "Web Service"
3. Подключите ваш GitHub репозиторий

#### Шаг 2: Настройка параметров
- **Name**: `ux-research-studio`
- **Environment**: `Python 3`
- **Build Command**: 
```bash
chmod +x build.sh
./build.sh
pip install -r requirements_web.txt
```
- **Start Command**: 
```bash
cd web_interface
gunicorn app:app --bind 0.0.0.0:$PORT --workers 1 --timeout 120
```

#### Шаг 3: Переменные окружения
В разделе "Environment Variables" добавьте:
- `OPENAI_API_KEY` = ваш API ключ OpenAI
- `RENDER` = `true`

### 3. Автоматический деплой с render.yaml

Если у вас есть файл `render.yaml` в корне репозитория:

1. В Render Dashboard выберите "New +" → "Blueprint"
2. Подключите репозиторий
3. Render автоматически создаст сервис на основе `render.yaml`

## 🔧 Локальная разработка

### Запуск локально
```bash
cd web_interface
pip install -r requirements_web.txt
python app.py
```

### Тестирование
Откройте http://localhost:5000

## 📊 Мониторинг

### Логи
- В Render Dashboard → ваш сервис → "Logs"
- Отслеживайте ошибки и производительность

### Health Check
- URL: `https://your-app.onrender.com/`
- Render автоматически проверяет доступность

## 🚨 Возможные проблемы

### 1. Chrome не устанавливается
```bash
# В build.sh добавьте:
apt-get install -y --no-install-recommends google-chrome-stable
```

### 2. Memory issues
- Увеличьте план до "Standard" (1GB RAM)
- Добавьте в startCommand: `--max-requests 1000 --max-requests-jitter 100`

### 3. Timeout issues
- Увеличьте timeout в gunicorn: `--timeout 300`
- Добавьте в config: `'page_load_timeout': 60`

## 🔄 Обновление

После изменения кода:
```bash
git add .
git commit -m "Update web interface"
git push origin main
```

Render автоматически пересоберет и перезапустит приложение.

## 📈 Масштабирование

### Автоматическое масштабирование
- В Render Dashboard → "Settings" → "Auto-Deploy"
- Включите "Auto-Deploy" для автоматических обновлений

### Ручное масштабирование
- Измените количество workers в startCommand
- Обновите план (Starter → Standard → Pro)

## 💰 Стоимость

- **Starter**: $7/месяц (512MB RAM, 0.1 CPU)
- **Standard**: $25/месяц (1GB RAM, 0.5 CPU)
- **Pro**: $50/месяц (2GB RAM, 1 CPU)

## 🎯 Готово!

После успешного деплоя вы получите URL вида:
`https://ux-research-studio.onrender.com`

Теперь можете:
1. Создавать UX исследования через веб-интерфейс
2. Отслеживать прогресс в реальном времени
3. Получать детальные отчеты
4. Делиться результатами с командой
