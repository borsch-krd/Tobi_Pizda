"""
Серверная часть сервиса синхронизированных заметок
"""
from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import os
import markdown
from datetime import datetime
import uuid

app = Flask(__name__)
DATABASE = '/workspace/server/notes.db'

def init_db():
    """Инициализация базы данных"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    # Таблица пользователей
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Таблица заметок
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS notes (
            id TEXT PRIMARY KEY,
            user_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    conn.commit()
    conn.close()

def get_db_connection():
    """Получить соединение с базой данных"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/api/register', methods=['POST'])
def register():
    """Регистрация нового пользователя"""
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({'error': 'Username and password are required'}), 400
    
    try:
        conn = get_db_connection()
        hashed_password = generate_password_hash(password)
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO users (username, password_hash) VALUES (?, ?)',
            (username, hashed_password)
        )
        conn.commit()
        user_id = cursor.lastrowid
        conn.close()
        
        return jsonify({
            'message': 'User registered successfully',
            'user_id': user_id
        }), 201
        
    except sqlite3.IntegrityError:
        return jsonify({'error': 'Username already exists'}), 409

@app.route('/api/login', methods=['POST'])
def login():
    """Аутентификация пользователя"""
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({'error': 'Username and password are required'}), 400
    
    conn = get_db_connection()
    user = conn.execute(
        'SELECT * FROM users WHERE username = ?', (username,)
    ).fetchone()
    conn.close()
    
    if user and check_password_hash(user['password_hash'], password):
        return jsonify({
            'message': 'Login successful',
            'user_id': user['id'],
            'username': user['username']
        }), 200
    else:
        return jsonify({'error': 'Invalid credentials'}), 401

@app.route('/api/notes', methods=['GET'])
def get_notes():
    """Получить все заметки пользователя"""
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({'error': 'User ID is required'}), 400
    
    conn = get_db_connection()
    notes = conn.execute(
        'SELECT * FROM notes WHERE user_id = ? ORDER BY updated_at DESC',
        (user_id,)
    ).fetchall()
    conn.close()
    
    notes_list = []
    for note in notes:
        notes_list.append({
            'id': note['id'],
            'title': note['title'],
            'content': note['content'],
            'created_at': note['created_at'],
            'updated_at': note['updated_at']
        })
    
    return jsonify({'notes': notes_list}), 200

@app.route('/api/notes/<note_id>', methods=['GET'])
def get_note(note_id):
    """Получить конкретную заметку"""
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({'error': 'User ID is required'}), 400
    
    conn = get_db_connection()
    note = conn.execute(
        'SELECT * FROM notes WHERE id = ? AND user_id = ?',
        (note_id, user_id)
    ).fetchone()
    conn.close()
    
    if note:
        return jsonify({
            'id': note['id'],
            'title': note['title'],
            'content': note['content'],
            'created_at': note['created_at'],
            'updated_at': note['updated_at']
        }), 200
    else:
        return jsonify({'error': 'Note not found'}), 404

@app.route('/api/notes', methods=['POST'])
def create_note():
    """Создать новую заметку"""
    data = request.get_json()
    user_id = data.get('user_id')
    title = data.get('title', 'Без названия')
    content = data.get('content', '')
    
    if not user_id:
        return jsonify({'error': 'User ID is required'}), 400
    
    note_id = str(uuid.uuid4())
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO notes (id, user_id, title, content)
        VALUES (?, ?, ?, ?)
    ''', (note_id, user_id, title, content))
    conn.commit()
    conn.close()
    
    return jsonify({
        'id': note_id,
        'title': title,
        'content': content,
        'created_at': datetime.now().isoformat(),
        'updated_at': datetime.now().isoformat()
    }), 201

@app.route('/api/notes/<note_id>', methods=['PUT'])
def update_note(note_id):
    """Обновить существующую заметку"""
    data = request.get_json()
    user_id = data.get('user_id')
    title = data.get('title')
    content = data.get('content')
    
    if not user_id:
        return jsonify({'error': 'User ID is required'}), 400
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Проверяем, что заметка принадлежит пользователю
    existing_note = cursor.execute(
        'SELECT * FROM notes WHERE id = ? AND user_id = ?',
        (note_id, user_id)
    ).fetchone()
    
    if not existing_note:
        conn.close()
        return jsonify({'error': 'Note not found or access denied'}), 404
    
    # Обновляем заметку
    cursor.execute('''
        UPDATE notes
        SET title = COALESCE(?, title), 
            content = COALESCE(?, content),
            updated_at = CURRENT_TIMESTAMP
        WHERE id = ? AND user_id = ?
    ''', (title, content, note_id, user_id))
    
    conn.commit()
    conn.close()
    
    return jsonify({
        'id': note_id,
        'title': title or existing_note['title'],
        'content': content or existing_note['content'],
        'updated_at': datetime.now().isoformat()
    }), 200

@app.route('/api/notes/<note_id>', methods=['DELETE'])
def delete_note(note_id):
    """Удалить заметку"""
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({'error': 'User ID is required'}), 400
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        'DELETE FROM notes WHERE id = ? AND user_id = ?',
        (note_id, user_id)
    )
    affected_rows = cursor.rowcount
    conn.commit()
    conn.close()
    
    if affected_rows > 0:
        return jsonify({'message': 'Note deleted successfully'}), 200
    else:
        return jsonify({'error': 'Note not found or access denied'}), 404

@app.route('/api/notes/<note_id>/html', methods=['GET'])
def get_note_html(note_id):
    """Получить заметку в формате HTML (рендеринг Markdown)"""
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({'error': 'User ID is required'}), 400
    
    conn = get_db_connection()
    note = conn.execute(
        'SELECT * FROM notes WHERE id = ? AND user_id = ?',
        (note_id, user_id)
    ).fetchone()
    conn.close()
    
    if note:
        html_content = markdown.markdown(note['content'], extensions=['extra', 'codehilite'])
        return jsonify({
            'id': note['id'],
            'title': note['title'],
            'html_content': html_content
        }), 200
    else:
        return jsonify({'error': 'Note not found'}), 404

if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=5000)