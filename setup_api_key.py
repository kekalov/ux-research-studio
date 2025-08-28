"""
Setup API Key - настройка API ключа OpenAI
"""

import os
import json
from pathlib import Path

def setup_api_key():
    """Настройка API ключа OpenAI"""
    
    print("🔑 НАСТРОЙКА API КЛЮЧА OPENAI")
    print("=" * 50)
    
    # Проверяем существующий ключ
    existing_key = os.getenv('OPENAI_API_KEY')
    if existing_key:
        print(f"✅ API ключ уже установлен: {existing_key[:10]}...")
        return True
    
    print("❌ API ключ не найден")
    print("\n💡 ВАРИАНТЫ УСТАНОВКИ:")
    print("1. Временная установка (только для текущей сессии)")
    print("2. Постоянная установка (сохранение в файл)")
    print("3. Ручная установка")
    
    choice = input("\nВыберите вариант (1-3): ").strip()
    
    if choice == "1":
        return setup_temporary_key()
    elif choice == "2":
        return setup_permanent_key()
    elif choice == "3":
        return setup_manual_key()
    else:
        print("❌ Неверный выбор")
        return False

def setup_temporary_key():
    """Временная установка ключа"""
    
    print("\n🔑 ВРЕМЕННАЯ УСТАНОВКА")
    print("Ключ будет доступен только в текущей сессии терминала")
    
    api_key = input("Введите ваш OpenAI API ключ: ").strip()
    
    if not api_key:
        print("❌ Ключ не введен")
        return False
    
    if not api_key.startswith('sk-'):
        print("❌ Неверный формат ключа (должен начинаться с 'sk-')")
        return False
    
    # Устанавливаем переменную окружения
    os.environ['OPENAI_API_KEY'] = api_key
    print(f"✅ API ключ установлен: {api_key[:10]}...")
    print("💡 Ключ будет доступен только в текущей сессии")
    
    return True

def setup_permanent_key():
    """Постоянная установка ключа"""
    
    print("\n🔑 ПОСТОЯННАЯ УСТАНОВКА")
    print("Ключ будет сохранен в файл .env")
    
    api_key = input("Введите ваш OpenAI API ключ: ").strip()
    
    if not api_key:
        print("❌ Ключ не введен")
        return False
    
    if not api_key.startswith('sk-'):
        print("❌ Неверный формат ключа (должен начинаться с 'sk-')")
        return False
    
    # Создаем файл .env
    env_file = Path('.env')
    env_content = f"OPENAI_API_KEY={api_key}\n"
    
    with open(env_file, 'w') as f:
        f.write(env_content)
    
    print(f"✅ API ключ сохранен в файл .env")
    print(f"💡 Файл: {env_file.absolute()}")
    print("💡 Перезапустите терминал для применения изменений")
    
    return True

def setup_manual_key():
    """Ручная установка ключа"""
    
    print("\n🔑 РУЧНАЯ УСТАНОВКА")
    print("Выполните одну из команд в терминале:")
    print()
    print("Для временной установки:")
    print("export OPENAI_API_KEY='your-api-key-here'")
    print()
    print("Для постоянной установки (добавьте в ~/.zshrc или ~/.bash_profile):")
    print("echo 'export OPENAI_API_KEY=\"your-api-key-here\"' >> ~/.zshrc")
    print("source ~/.zshrc")
    print()
    print("💡 Замените 'your-api-key-here' на ваш реальный ключ")
    
    return False

def test_api_key():
    """Тест API ключа"""
    
    print("\n🧪 ТЕСТИРОВАНИЕ API КЛЮЧА")
    print("=" * 50)
    
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("❌ API ключ не найден")
        return False
    
    try:
        import openai
        
        client = openai.OpenAI(api_key=api_key)
        
        # Простой тест
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": "Привет! Это тест API ключа."}
            ],
            max_tokens=30
        )
        
        print("✅ API ключ работает!")
        print(f"Ответ: {response.choices[0].message.content}")
        return True
        
    except Exception as e:
        print(f"❌ Ошибка API: {e}")
        return False

def main():
    """Основная функция"""
    
    print("🔧 НАСТРОЙКА OPENAI API КЛЮЧА")
    print("=" * 60)
    
    # Настраиваем ключ
    if setup_api_key():
        # Тестируем ключ
        if test_api_key():
            print("\n🎉 Настройка завершена успешно!")
            print("Теперь вы можете использовать OpenAI в агентах")
        else:
            print("\n❌ Проблема с API ключом")
    else:
        print("\n💡 Выполните ручную настройку и перезапустите скрипт")

if __name__ == "__main__":
    main()


