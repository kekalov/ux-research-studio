"""
Load Environment - загрузка переменных окружения
"""

import os
from pathlib import Path

def load_env_file():
    """Загрузка переменных из файла .env"""
    
    env_file = Path('.env')
    if not env_file.exists():
        print("❌ Файл .env не найден")
        return False
    
    print("📁 Загружаем переменные из .env файла...")
    
    with open(env_file, 'r') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#'):
                if '=' in line:
                    key, value = line.split('=', 1)
                    os.environ[key] = value
                    print(f"✅ Загружено: {key}={value[:10]}...")
    
    return True

def check_api_key():
    """Проверка API ключа"""
    
    api_key = os.getenv('OPENAI_API_KEY')
    if api_key:
        print(f"✅ API ключ найден: {api_key[:10]}...")
        return True
    else:
        print("❌ API ключ не найден")
        return False

def test_openai():
    """Тест OpenAI API"""
    
    try:
        import openai
        
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            print("❌ API ключ не найден")
            return False
        
        client = openai.OpenAI(api_key=api_key)
        
        # Простой тест
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "Привет! Это тест API."}],
            max_tokens=20
        )
        
        print("✅ OpenAI API работает!")
        print(f"Ответ: {response.choices[0].message.content}")
        return True
        
    except Exception as e:
        print(f"❌ Ошибка OpenAI: {e}")
        return False

if __name__ == "__main__":
    print("🔧 ЗАГРУЗКА ПЕРЕМЕННЫХ ОКРУЖЕНИЯ")
    print("=" * 50)
    
    if load_env_file():
        if check_api_key():
            print("\n🧪 Тестируем OpenAI API...")
            test_openai()
        else:
            print("\n💡 Отредактируйте файл .env и добавьте ваш API ключ")
    else:
        print("\n💡 Создайте файл .env с вашим API ключом")


