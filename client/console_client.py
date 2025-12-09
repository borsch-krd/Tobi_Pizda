"""
Консольный клиент для сервиса синхронизированных заметок
"""
import requests
import json
import os
from datetime import datetime

# Адрес сервера
BASE_URL = 'http://localhost:5000/api'

class NotesClient:
    def __init__(self, base_url=BASE_URL):
        self.base_url = base_url
        self.user_id = None
        self.username = None
        self.session = requests.Session()

    def register(self, username, password):
        """Регистрация нового пользователя"""
        url = f"{self.base_url}/register"
        data = {
            'username': username,
            'password': password
        }
        
        try:
            response = self.session.post(url, json=data)
            if response.status_code == 201:
                result = response.json()
                self.user_id = result['user_id']
                self.username = username
                print(f"Пользователь {username} успешно зарегистрирован!")
                return True
            else:
                print(f"Ошибка регистрации: {response.json().get('error', 'Неизвестная ошибка')}")
                return False
        except Exception as e:
            print(f"Ошибка подключения к серверу: {e}")
            return False

    def login(self, username, password):
        """Аутентификация пользователя"""
        url = f"{self.base_url}/login"
        data = {
            'username': username,
            'password': password
        }
        
        try:
            response = self.session.post(url, json=data)
            if response.status_code == 200:
                result = response.json()
                self.user_id = result['user_id']
                self.username = result['username']
                print(f"Добро пожаловать, {self.username}!")
                return True
            else:
                print(f"Ошибка входа: {response.json().get('error', 'Неизвестная ошибка')}")
                return False
        except Exception as e:
            print(f"Ошибка подключения к серверу: {e}")
            return False

    def create_note(self, title, content):
        """Создать новую заметку"""
        if not self.user_id:
            print("Сначала войдите в систему")
            return False
            
        url = f"{self.base_url}/notes"
        data = {
            'user_id': self.user_id,
            'title': title,
            'content': content
        }
        
        try:
            response = self.session.post(url, json=data)
            if response.status_code == 201:
                result = response.json()
                print(f"Заметка '{result['title']}' создана с ID: {result['id']}")
                return True
            else:
                print(f"Ошибка создания заметки: {response.json().get('error', 'Неизвестная ошибка')}")
                return False
        except Exception as e:
            print(f"Ошибка подключения к серверу: {e}")
            return False

    def get_notes(self):
        """Получить все заметки пользователя"""
        if not self.user_id:
            print("Сначала войдите в систему")
            return []
            
        url = f"{self.base_url}/notes?user_id={self.user_id}"
        
        try:
            response = self.session.get(url)
            if response.status_code == 200:
                result = response.json()
                return result['notes']
            else:
                print(f"Ошибка получения заметок: {response.json().get('error', 'Неизвестная ошибка')}")
                return []
        except Exception as e:
            print(f"Ошибка подключения к серверу: {e}")
            return []

    def get_note(self, note_id):
        """Получить конкретную заметку"""
        if not self.user_id:
            print("Сначала войдите в систему")
            return None
            
        url = f"{self.base_url}/notes/{note_id}?user_id={self.user_id}"
        
        try:
            response = self.session.get(url)
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Ошибка получения заметки: {response.json().get('error', 'Неизвестная ошибка')}")
                return None
        except Exception as e:
            print(f"Ошибка подключения к серверу: {e}")
            return None

    def update_note(self, note_id, title=None, content=None):
        """Обновить заметку"""
        if not self.user_id:
            print("Сначала войдите в систему")
            return False
            
        url = f"{self.base_url}/notes/{note_id}"
        data = {
            'user_id': self.user_id
        }
        if title is not None:
            data['title'] = title
        if content is not None:
            data['content'] = content
        
        try:
            response = self.session.put(url, json=data)
            if response.status_code == 200:
                result = response.json()
                print(f"Заметка обновлена: {result['title']}")
                return True
            else:
                print(f"Ошибка обновления заметки: {response.json().get('error', 'Неизвестная ошибка')}")
                return False
        except Exception as e:
            print(f"Ошибка подключения к серверу: {e}")
            return False

    def delete_note(self, note_id):
        """Удалить заметку"""
        if not self.user_id:
            print("Сначала войдите в систему")
            return False
            
        url = f"{self.base_url}/notes/{note_id}?user_id={self.user_id}"
        
        try:
            response = self.session.delete(url)
            if response.status_code == 200:
                print("Заметка успешно удалена")
                return True
            else:
                print(f"Ошибка удаления заметки: {response.json().get('error', 'Неизвестная ошибка')}")
                return False
        except Exception as e:
            print(f"Ошибка подключения к серверу: {e}")
            return False

def print_menu():
    """Вывести меню приложения"""
    print("\n=== Меню сервиса заметок ===")
    print("1. Регистрация")
    print("2. Вход")
    print("3. Создать заметку")
    print("4. Просмотреть все заметки")
    print("5. Просмотреть конкретную заметку")
    print("6. Обновить заметку")
    print("7. Удалить заметку")
    print("8. Выход")
    print("=============================")

def main():
    client = NotesClient()
    
    while True:
        print_menu()
        choice = input("Выберите действие (1-8): ").strip()
        
        if choice == '1':
            # Регистрация
            username = input("Введите имя пользователя: ").strip()
            password = input("Введите пароль: ").strip()
            client.register(username, password)
            
        elif choice == '2':
            # Вход
            username = input("Введите имя пользователя: ").strip()
            password = input("Введите пароль: ").strip()
            client.login(username, password)
            
        elif choice == '3':
            # Создать заметку
            title = input("Введите заголовок заметки: ").strip()
            if not title:
                title = "Без названия"
            content = input("Введите содержимое заметки (в формате Markdown): ").strip()
            client.create_note(title, content)
            
        elif choice == '4':
            # Просмотреть все заметки
            notes = client.get_notes()
            if notes:
                print(f"\nВаши заметки ({len(notes)}):")
                for note in notes:
                    print(f"- ID: {note['id'][:8]}... | {note['title']} | Обновлено: {note['updated_at']}")
            else:
                print("У вас пока нет заметок.")
                
        elif choice == '5':
            # Просмотреть конкретную заметку
            note_id = input("Введите ID заметки: ").strip()
            note = client.get_note(note_id)
            if note:
                print(f"\nЗаметка: {note['title']}")
                print(f"ID: {note['id']}")
                print(f"Создано: {note['created_at']}")
                print(f"Обновлено: {note['updated_at']}")
                print(f"Содержимое:\n{note['content']}")
            else:
                print("Заметка не найдена или ошибка доступа.")
                
        elif choice == '6':
            # Обновить заметку
            note_id = input("Введите ID заметки для обновления: ").strip()
            note = client.get_note(note_id)
            if note:
                print(f"Текущая заметка: {note['title']}")
                new_title = input(f"Новый заголовок (Enter для пропуска, текущий: {note['title']}): ").strip()
                new_content = input("Новое содержимое (Enter для пропуска): ").strip()
                
                title = new_title if new_title else None
                content = new_content if new_content else None
                
                if title is not None or content is not None:
                    client.update_note(note_id, title, content)
                else:
                    print("Нечего обновлять.")
            else:
                print("Заметка не найдена или ошибка доступа.")
                
        elif choice == '7':
            # Удалить заметку
            note_id = input("Введите ID заметки для удаления: ").strip()
            confirm = input(f"Вы уверены, что хотите удалить заметку {note_id}? (y/N): ").strip().lower()
            if confirm == 'y':
                client.delete_note(note_id)
                
        elif choice == '8':
            # Выход
            print("До свидания!")
            break
            
        else:
            print("Неверный выбор. Пожалуйста, выберите от 1 до 8.")

if __name__ == "__main__":
    main()