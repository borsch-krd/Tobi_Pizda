#!/usr/bin/env python3
"""
Тестирование API сервиса синхронизированных заметок
"""
import requests
import json
import time

BASE_URL = 'http://localhost:5000/api'

def test_api():
    print("Тестирование API сервиса заметок...")
    print(f"Базовый URL: {BASE_URL}")
    
    # Регистрация пользователя
    print("\n1. Регистрация пользователя...")
    register_data = {
        'username': 'test_user',
        'password': 'test_password'
    }
    
    try:
        response = requests.post(f"{BASE_URL}/register", json=register_data)
        if response.status_code == 201:
            user_data = response.json()
            user_id = user_data['user_id']
            print(f"  ✓ Пользователь зарегистрирован. ID: {user_id}")
        else:
            print(f"  ✗ Ошибка регистрации: {response.json()}")
            return False
    except Exception as e:
        print(f"  ✗ Ошибка подключения: {e}")
        return False
    
    # Вход пользователя
    print("\n2. Вход пользователя...")
    login_data = {
        'username': 'test_user',
        'password': 'test_password'
    }
    
    try:
        response = requests.post(f"{BASE_URL}/login", json=login_data)
        if response.status_code == 200:
            login_result = response.json()
            print(f"  ✓ Вход выполнен. Пользователь: {login_result['username']}")
        else:
            print(f"  ✗ Ошибка входа: {response.json()}")
            return False
    except Exception as e:
        print(f"  ✗ Ошибка подключения: {e}")
        return False
    
    # Создание заметки
    print("\n3. Создание заметки...")
    note_data = {
        'user_id': user_id,
        'title': 'Тестовая заметка',
        'content': '# Заголовок\n\nЭто **тестовая** заметка в формате *Markdown*.\n\n- Элемент списка 1\n- Элемент списка 2\n\n```python\nprint("Hello, World!")\n```'
    }
    
    try:
        response = requests.post(f"{BASE_URL}/notes", json=note_data)
        if response.status_code == 201:
            note = response.json()
            note_id = note['id']
            print(f"  ✓ Заметка создана. ID: {note_id[:8]}...")
        else:
            print(f"  ✗ Ошибка создания заметки: {response.json()}")
            return False
    except Exception as e:
        print(f"  ✗ Ошибка подключения: {e}")
        return False
    
    # Получение всех заметок
    print("\n4. Получение всех заметок...")
    try:
        response = requests.get(f"{BASE_URL}/notes?user_id={user_id}")
        if response.status_code == 200:
            notes = response.json()['notes']
            print(f"  ✓ Получено {len(notes)} заметок")
            if len(notes) > 0:
                print(f"    Первая заметка: {notes[0]['title']}")
        else:
            print(f"  ✗ Ошибка получения заметок: {response.json()}")
            return False
    except Exception as e:
        print(f"  ✗ Ошибка подключения: {e}")
        return False
    
    # Получение конкретной заметки
    print("\n5. Получение конкретной заметки...")
    try:
        response = requests.get(f"{BASE_URL}/notes/{note_id}?user_id={user_id}")
        if response.status_code == 200:
            note = response.json()
            print(f"  ✓ Заметка получена: {note['title']}")
        else:
            print(f"  ✗ Ошибка получения заметки: {response.json()}")
            return False
    except Exception as e:
        print(f"  ✗ Ошибка подключения: {e}")
        return False
    
    # Обновление заметки
    print("\n6. Обновление заметки...")
    update_data = {
        'user_id': user_id,
        'title': 'Обновленная тестовая заметка',
        'content': '# Обновленный заголовок\n\nЭто **обновленная** заметка в формате *Markdown*.\n\n- Обновленный элемент списка 1\n- Обновленный элемент списка 2'
    }
    
    try:
        response = requests.put(f"{BASE_URL}/notes/{note_id}", json=update_data)
        if response.status_code == 200:
            updated_note = response.json()
            print(f"  ✓ Заметка обновлена: {updated_note['title']}")
        else:
            print(f"  ✗ Ошибка обновления заметки: {response.json()}")
            return False
    except Exception as e:
        print(f"  ✗ Ошибка подключения: {e}")
        return False
    
    # Получение заметки в формате HTML
    print("\n7. Получение заметки в формате HTML...")
    try:
        response = requests.get(f"{BASE_URL}/notes/{note_id}/html?user_id={user_id}")
        if response.status_code == 200:
            html_note = response.json()
            print(f"  ✓ Заметка получена в формате HTML: {html_note['title']}")
            # Показываем первые 100 символов HTML
            html_preview = html_note['html_content'][:100].replace('\n', ' ')
            print(f"    HTML preview: {html_preview}...")
        else:
            print(f"  ✗ Ошибка получения HTML: {response.json()}")
            return False
    except Exception as e:
        print(f"  ✗ Ошибка подключения: {e}")
        return False
    
    # Удаление заметки
    print("\n8. Удаление заметки...")
    try:
        response = requests.delete(f"{BASE_URL}/notes/{note_id}?user_id={user_id}")
        if response.status_code == 200:
            print(f"  ✓ Заметка удалена")
        else:
            print(f"  ✗ Ошибка удаления заметки: {response.json()}")
            return False
    except Exception as e:
        print(f"  ✗ Ошибка подключения: {e}")
        return False
    
    # Проверка, что заметка действительно удалена
    print("\n9. Проверка удаления заметки...")
    try:
        response = requests.get(f"{BASE_URL}/notes/{note_id}?user_id={user_id}")
        if response.status_code == 404:
            print(f"  ✓ Заметка действительно удалена (возвращена ошибка 404)")
        else:
            print(f"  ✗ Заметка не удалена: {response.status_code}")
            return False
    except Exception as e:
        print(f"  ✗ Ошибка подключения: {e}")
        return False
    
    print("\n✓ Все тесты пройдены успешно!")
    return True

if __name__ == "__main__":
    test_api()