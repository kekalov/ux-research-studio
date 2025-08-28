"""
Quick Setup - быстрая настройка API ключа
"""

import os

def quick_setup():
    """Быстрая настройка API ключа"""
    
    print("🔑 БЫСТРАЯ НАСТРОЙКА API КЛЮЧА")
    print("=" * 40)
    
    # Проверяем существующий ключ
    existing_key = os.getenv('OPENAI_API_KEY')
    if existing_key:
        print(f"✅ API ключ уже установлен: {existing_key[:10]}...")
        return True
    
    print("❌ API ключ не найден")
    print("\n💡 ВАШИ ДЕЙСТВИЯ:")
    print("1. Скопируйте ваш API ключ")
    print("2. Выполните команду в терминале:")
    print("   export OPENAI_API_KEY='sk-your-key-here'")
    print("3. Замените 'sk-your-key-here' на ваш реальный ключ")
    print("4. Перезапустите этот скрипт")
    
    return False

def test_key():
    """Тест API ключа"""
    
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
            messages=[{"role": "user", "content": "Привет! Тест API."}],
            max_tokens=20
        )
        
        print("✅ API ключ работает!")
        print(f"Ответ: {response.choices[0].message.content}")
        return True
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return False

if __name__ == "__main__":
    if quick_setup():
        test_key()
    else:
        print("\n💡 После установки ключа запустите:")
        print("python quick_setup.py")


