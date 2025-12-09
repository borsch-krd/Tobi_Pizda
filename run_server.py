#!/usr/bin/env python3
"""
Скрипт для запуска сервера сервиса заметок
"""
import subprocess
import sys
import time
import os

def run_server():
    """Запуск сервера в фоновом режиме"""
    try:
        # Запускаем сервер в фоновом режиме
        server_process = subprocess.Popen([
            sys.executable, 
            '/workspace/server/app.py'
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        print(f"Сервер запущен с PID: {server_process.pid}")
        print("Сервер доступен по адресу: http://localhost:5000")
        
        # Ждем несколько секунд, чтобы сервер успел запуститься
        time.sleep(2)
        
        # Проверяем, запустился ли сервер
        if server_process.poll() is None:
            print("Сервер успешно запущен и работает")
            return server_process
        else:
            stdout, stderr = server_process.communicate()
            print(f"Ошибка при запуске сервера: {stderr.decode()}")
            return None
            
    except Exception as e:
        print(f"Ошибка при запуске сервера: {e}")
        return None

if __name__ == "__main__":
    print("Запуск сервера сервиса заметок...")
    server_process = run_server()
    
    if server_process:
        try:
            # Оставляем сервер работать
            print("Сервер работает. Нажмите Ctrl+C для остановки.")
            server_process.wait()
        except KeyboardInterrupt:
            print("\nОстановка сервера...")
            server_process.terminate()
            server_process.wait()
            print("Сервер остановлен.")
    else:
        print("Не удалось запустить сервер.")
        sys.exit(1)