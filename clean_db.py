#!/usr/bin/env python3
"""
Скрипт для очистки базы данных
"""
import os
import sqlite3

def clean_database():
    db_path = '/workspace/server/notes.db'
    
    if os.path.exists(db_path):
        print(f"Удаление существующей базы данных: {db_path}")
        os.remove(db_path)
        print("База данных удалена")
    else:
        print("База данных не найдена, создание новой...")

if __name__ == "__main__":
    clean_database()