"""
Fix OpenAI - диагностика и исправление проблем с OpenAI API
"""

import sys
import os
import subprocess

def check_python_environment():
    """Проверка Python окружения"""
    
    print("🔍 ДИАГНОСТИКА PYTHON ОКРУЖЕНИЯ")
    print("=" * 50)
    
    print(f"Python версия: {sys.version}")
    print(f"Python путь: {sys.executable}")
    print(f"Пути поиска модулей:")
    for path in sys.path:
        print(f"  - {path}")
    
    print(f"\nПеременные окружения:")
    print(f"PYTHONPATH: {os.getenv('PYTHONPATH', 'Не установлен')}")
    print(f"CONDA_DEFAULT_ENV: {os.getenv('CONDA_DEFAULT_ENV', 'Не установлен')}")

def check_openai_installation():
    """Проверка установки OpenAI"""
    
    print(f"\n🔍 ПРОВЕРКА УСТАНОВКИ OPENAI")
    print("=" * 50)
    
    try:
        import openai
        print(f"✅ OpenAI установлен: {openai.__version__}")
        print(f"Путь к модулю: {openai.__file__}")
    except ImportError as e:
        print(f"❌ OpenAI не установлен: {e}")
        return False
    
    return True

def check_openai_api_key():
    """Проверка API ключа OpenAI"""
    
    print(f"\n🔑 ПРОВЕРКА API КЛЮЧА")
    print("=" * 50)
    
    api_key = os.getenv('OPENAI_API_KEY')
    if api_key:
        print(f"✅ API ключ найден: {api_key[:10]}...")
        return True
    else:
        print(f"❌ API ключ не найден")
        print(f"💡 Установите переменную окружения:")
        print(f"   export OPENAI_API_KEY='your-api-key-here'")
        return False

def install_openai_in_conda():
    """Установка OpenAI в conda окружении"""
    
    print(f"\n📦 УСТАНОВКА OPENAI В CONDA")
    print("=" * 50)
    
    try:
        # Пробуем установить через conda
        result = subprocess.run(['conda', 'install', 'openai', '-c', 'conda-forge', '-y'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ OpenAI установлен через conda")
            return True
        else:
            print(f"❌ Ошибка conda: {result.stderr}")
            
        # Пробуем через pip в conda
        result = subprocess.run([sys.executable, '-m', 'pip', 'install', 'openai'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ OpenAI установлен через pip")
            return True
        else:
            print(f"❌ Ошибка pip: {result.stderr}")
            
    except Exception as e:
        print(f"❌ Ошибка установки: {e}")
    
    return False

def test_openai_functionality():
    """Тест функциональности OpenAI"""
    
    print(f"\n🧪 ТЕСТ ФУНКЦИОНАЛЬНОСТИ OPENAI")
    print("=" * 50)
    
    try:
        import openai
        
        # Проверяем API ключ
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            print("❌ API ключ не найден - тест пропущен")
            return False
        
        # Создаем клиент
        client = openai.OpenAI(api_key=api_key)
        print("✅ Клиент OpenAI создан")
        
        # Простой тест (без реального запроса)
        print("✅ OpenAI готов к использованию")
        return True
        
    except Exception as e:
        print(f"❌ Ошибка тестирования: {e}")
        return False

def create_demo_with_openai():
    """Создание демо с использованием OpenAI"""
    
    print(f"\n🤖 ДЕМО С OPENAI")
    print("=" * 50)
    
    try:
        import openai
        
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            print("❌ API ключ не найден")
            return
        
        client = openai.OpenAI(api_key=api_key)
        
        # Простой запрос для теста
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": "Привет! Как дела?"}
            ],
            max_tokens=50
        )
        
        print("✅ OpenAI работает!")
        print(f"Ответ: {response.choices[0].message.content}")
        
    except Exception as e:
        print(f"❌ Ошибка OpenAI: {e}")

def main():
    """Основная функция диагностики"""
    
    print("🔧 ДИАГНОСТИКА И ИСПРАВЛЕНИЕ OPENAI")
    print("=" * 60)
    
    # Проверяем окружение
    check_python_environment()
    
    # Проверяем установку
    openai_installed = check_openai_installation()
    
    if not openai_installed:
        print(f"\n📦 УСТАНАВЛИВАЕМ OPENAI...")
        install_openai_in_conda()
        check_openai_installation()
    
    # Проверяем API ключ
    api_key_ok = check_openai_api_key()
    
    # Тестируем функциональность
    if openai_installed and api_key_ok:
        test_openai_functionality()
        create_demo_with_openai()
    
    print(f"\n💡 РЕКОМЕНДАЦИИ:")
    print(f"1. Убедитесь, что используете правильное Python окружение")
    print(f"2. Установите API ключ: export OPENAI_API_KEY='your-key'")
    print(f"3. Перезапустите терминал после установки переменных")
    print(f"4. Если проблемы остаются, используйте demo_agent_simple.py")

if __name__ == "__main__":
    main()


