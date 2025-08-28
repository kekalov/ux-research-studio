#!/usr/bin/env python3
"""
Скрипт для автоматического деплоя UX Research Studio на Render
"""

import os
import subprocess
import sys
from pathlib import Path

def run_command(command, description):
    """Выполнение команды с выводом"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} - успешно!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} - ошибка!")
        print(f"Ошибка: {e.stderr}")
        return False

def check_git_status():
    """Проверка статуса git"""
    print("🔍 Проверка статуса Git...")
    
    # Проверяем, что мы в git репозитории
    if not Path('.git').exists():
        print("❌ Не найден .git репозиторий!")
        print("Убедитесь, что вы находитесь в корневой папке проекта")
        return False
    
    # Проверяем статус
    result = subprocess.run('git status --porcelain', shell=True, capture_output=True, text=True)
    
    if result.stdout.strip():
        print("📝 Найдены несохраненные изменения:")
        print(result.stdout)
        return False
    else:
        print("✅ Все изменения сохранены")
        return True

def deploy_to_render():
    """Основная функция деплоя"""
    print("🚀 ДЕПЛОЙ UX RESEARCH STUDIO НА RENDER")
    print("=" * 50)
    
    # Проверяем статус git
    if not check_git_status():
        print("\n💡 Для продолжения:")
        print("1. Сохраните все изменения: git add . && git commit -m 'Update'")
        print("2. Запустите скрипт снова")
        return False
    
    # Проверяем наличие необходимых файлов
    required_files = [
        'web_interface/app.py',
        'web_interface/requirements_web.txt',
        'web_interface/build.sh',
        'web_interface/render.yaml'
    ]
    
    print("\n📁 Проверка файлов...")
    for file_path in required_files:
        if Path(file_path).exists():
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path} - не найден!")
            return False
    
    # Проверяем переменные окружения
    print("\n🔑 Проверка переменных окружения...")
    openai_key = os.getenv('OPENAI_API_KEY')
    if openai_key:
        print("✅ OPENAI_API_KEY найден")
    else:
        print("⚠️  OPENAI_API_KEY не найден")
        print("Убедитесь, что ключ установлен в Render Dashboard")
    
    # Показываем инструкции
    print("\n📋 ИНСТРУКЦИИ ПО ДЕПЛОЮ:")
    print("=" * 50)
    print("1. Зайдите на https://render.com")
    print("2. Нажмите 'New +' → 'Web Service'")
    print("3. Подключите ваш GitHub репозиторий")
    print("4. Настройте параметры:")
    print("   - Name: ux-research-studio")
    print("   - Environment: Python 3")
    print("   - Build Command: chmod +x build.sh && ./build.sh && pip install -r requirements_web.txt")
    print("   - Start Command: cd web_interface && gunicorn app:app --bind 0.0.0.0:$PORT --workers 1 --timeout 120")
    print("5. Добавьте переменные окружения:")
    print("   - OPENAI_API_KEY = ваш ключ")
    print("   - RENDER = true")
    print("6. Нажмите 'Create Web Service'")
    
    print("\n🎯 АЛЬТЕРНАТИВНО - Автоматический деплой:")
    print("1. В Render Dashboard выберите 'New +' → 'Blueprint'")
    print("2. Подключите репозиторий")
    print("3. Render автоматически создаст сервис на основе render.yaml")
    
    print("\n🔗 После деплоя:")
    print("- URL будет: https://your-app-name.onrender.com")
    print("- Логи: Render Dashboard → ваш сервис → 'Logs'")
    print("- Обновления: просто push в git")
    
    return True

def test_local():
    """Тестирование локально"""
    print("🧪 ТЕСТИРОВАНИЕ ЛОКАЛЬНО")
    print("=" * 30)
    
    # Проверяем Python
    if not run_command('python3 --version', 'Проверка Python'):
        return False
    
    # Устанавливаем зависимости
    if not run_command('cd web_interface && pip install -r requirements_web.txt', 'Установка зависимостей'):
        return False
    
    # Запускаем сервер
    print("🌐 Запуск локального сервера...")
    print("Откройте http://localhost:5001")
    print("Для остановки нажмите Ctrl+C")
    
    try:
        subprocess.run('cd web_interface && python3 app.py', shell=True)
    except KeyboardInterrupt:
        print("\n⏹️ Сервер остановлен")
    
    return True

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'test':
        test_local()
    else:
        deploy_to_render()
