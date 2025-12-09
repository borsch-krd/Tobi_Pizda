#!/usr/bin/env python3
"""
Скрипт для создания дистрибутива проекта
"""
import os
import shutil
import zipfile
from datetime import datetime

def create_distribution():
    """Создание дистрибутива проекта"""
    print("Создание дистрибутива проекта...")
    
    # Создаем директорию для дистрибутива
    dist_dir = '/workspace/dist'
    if os.path.exists(dist_dir):
        shutil.rmtree(dist_dir)
    os.makedirs(dist_dir, exist_ok=True)
    
    # Список файлов и директорий для включения в дистрибутив
    items_to_include = [
        'server',
        'client',
        'common',
        'README.md',
        'ARCHITECTURE.md',
        'INSTALL.md',
        'SUMMARY.md',
        'MOBILE_DESKTOP_APPS.md',
        'run_server.py',
        'test_api.py',
        'full_test.py',
        'clean_db.py',
        'build_dist.py'
    ]
    
    # Создаем архив с проектом
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    archive_name = f'notes_service_{timestamp}.zip'
    archive_path = os.path.join(dist_dir, archive_name)
    
    with zipfile.ZipFile(archive_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for item in items_to_include:
            item_path = f'/workspace/{item}'
            if os.path.isdir(item_path):
                for root, dirs, files in os.walk(item_path):
                    for file in files:
                        file_path = os.path.join(root, file)
                        arc_path = os.path.relpath(file_path, '/workspace')
                        zipf.write(file_path, arc_path)
            elif os.path.isfile(item_path):
                arc_path = os.path.relpath(item_path, '/workspace')
                zipf.write(item_path, arc_path)
    
    print(f"Дистрибутив создан: {archive_path}")
    print(f"Размер архива: {os.path.getsize(archive_path)} байт")
    
    return archive_path

def main():
    try:
        archive_path = create_distribution()
        print(f"\n✓ Дистрибутив успешно создан: {archive_path}")
    except Exception as e:
        print(f"✗ Ошибка при создании дистрибутива: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())