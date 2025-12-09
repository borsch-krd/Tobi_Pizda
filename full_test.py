#!/usr/bin/env python3
"""
Полный тест сервиса синхронизированных заметок
Запускает сервер, выполняет тесты API и завершает работу
"""
import subprocess
import sys
import time
import requests
import signal
import os

def start_server():
    """Запуск сервера в фоновом режиме"""
    print("Запуск сервера...")
    server_process = subprocess.Popen([
        sys.executable, 
        '/workspace/server/app.py'
    ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    # Ждем, пока сервер запустится
    time.sleep(3)
    
    # Проверяем, запустился ли сервер
    if server_process.poll() is not None:
        stdout, stderr = server_process.communicate()
        print(f"Ошибка запуска сервера: {stderr.decode()}")
        return None
    
    print(f"Сервер запущен с PID: {server_process.pid}")
    return server_process

def wait_for_server_ready():
    """Ожидание готовности сервера к работе"""
    print("Ожидание готовности сервера...")
    for i in range(10):  # Попробуем 10 раз
        try:
            response = requests.get('http://localhost:5000/api/notes?user_id=1', timeout=5)
            # Сервер готов, если он отвечает, даже если с ошибкой
            print("Сервер готов к работе")
            return True
        except requests.exceptions.ConnectionError:
            print(f"Сервер еще не готов, ждем... ({i+1}/10)")
            time.sleep(1)
    
    print("Сервер не ответил в течение отведенного времени")
    return False

def run_tests():
    """Запуск тестов API"""
    print("Запуск тестов API...")
    try:
        result = subprocess.run([
            sys.executable, 
            '/workspace/test_api.py'
        ], capture_output=True, text=True)
        
        print("STDOUT:", result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)
        
        return result.returncode == 0
    except Exception as e:
        print(f"Ошибка при запуске тестов: {e}")
        return False

def stop_server(server_process):
    """Остановка сервера"""
    print("Остановка сервера...")
    try:
        server_process.terminate()
        server_process.wait(timeout=5)
    except subprocess.TimeoutExpired:
        print("Сервер не остановился вовремя, принудительно завершаем...")
        server_process.kill()
        server_process.wait()
    print("Сервер остановлен")

def main():
    print("=== Полное тестирование сервиса синхронизированных заметок ===")
    
    # Запускаем сервер
    server_process = start_server()
    if not server_process:
        print("Не удалось запустить сервер")
        sys.exit(1)
    
    # Ждем готовности сервера
    if not wait_for_server_ready():
        stop_server(server_process)
        sys.exit(1)
    
    # Запускаем тесты
    success = run_tests()
    
    # Останавливаем сервер
    stop_server(server_process)
    
    if success:
        print("\n✓ Все тесты прошли успешно!")
        return 0
    else:
        print("\n✗ Тесты завершились с ошибками")
        return 1

if __name__ == "__main__":
    sys.exit(main())