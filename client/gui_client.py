"""
GUI клиент для сервиса синхронизированных заметок
Использует PyQt5 для создания графического интерфейса
"""
import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QTextEdit, QPushButton, QListWidget, 
                             QLineEdit, QLabel, QMessageBox, QSplitter, QMenuBar, 
                             QMenu, QAction, QStatusBar)
from PyQt5.QtCore import Qt
import requests
import json

class NotesAPI:
    """Класс для работы с API сервиса заметок"""
    def __init__(self, base_url="http://localhost:5000/api"):
        self.base_url = base_url
        self.session = requests.Session()
        self.user_id = None
        self.username = None

    def register(self, username, password):
        """Регистрация нового пользователя"""
        try:
            response = self.session.post(f"{self.base_url}/register", json={
                'username': username,
                'password': password
            })
            if response.status_code == 201:
                result = response.json()
                self.user_id = result['user_id']
                self.username = username
                return True, result
            else:
                return False, response.json()
        except Exception as e:
            return False, str(e)

    def login(self, username, password):
        """Аутентификация пользователя"""
        try:
            response = self.session.post(f"{self.base_url}/login", json={
                'username': username,
                'password': password
            })
            if response.status_code == 200:
                result = response.json()
                self.user_id = result['user_id']
                self.username = result['username']
                return True, result
            else:
                return False, response.json()
        except Exception as e:
            return False, str(e)

    def get_notes(self):
        """Получить все заметки пользователя"""
        if not self.user_id:
            return False, "Пользователь не авторизован"
        
        try:
            response = self.session.get(f"{self.base_url}/notes", params={
                'user_id': self.user_id
            })
            if response.status_code == 200:
                return True, response.json()['notes']
            else:
                return False, response.json()
        except Exception as e:
            return False, str(e)

    def create_note(self, title, content):
        """Создать новую заметку"""
        if not self.user_id:
            return False, "Пользователь не авторизован"
        
        try:
            response = self.session.post(f"{self.base_url}/notes", json={
                'user_id': self.user_id,
                'title': title,
                'content': content
            })
            if response.status_code == 201:
                return True, response.json()
            else:
                return False, response.json()
        except Exception as e:
            return False, str(e)

    def update_note(self, note_id, title, content):
        """Обновить заметку"""
        if not self.user_id:
            return False, "Пользователь не авторизован"
        
        try:
            response = self.session.put(f"{self.base_url}/notes/{note_id}", json={
                'user_id': self.user_id,
                'title': title,
                'content': content
            })
            if response.status_code == 200:
                return True, response.json()
            else:
                return False, response.json()
        except Exception as e:
            return False, str(e)

    def delete_note(self, note_id):
        """Удалить заметку"""
        if not self.user_id:
            return False, "Пользователь не авторизован"
        
        try:
            response = self.session.delete(f"{self.base_url}/notes/{note_id}", params={
                'user_id': self.user_id
            })
            if response.status_code == 200:
                return True, response.json()
            else:
                return False, response.json()
        except Exception as e:
            return False, str(e)

class NotesApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.api = NotesAPI()
        self.current_note_id = None
        self.init_ui()
        
    def init_ui(self):
        self.setWindowTitle("Сервис синхронизированных заметок")
        self.setGeometry(100, 100, 1000, 700)
        
        # Центральный виджет
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Основной layout
        main_layout = QHBoxLayout(central_widget)
        
        # Левая панель с кнопками и списком заметок
        left_panel = QVBoxLayout()
        
        # Панель аутентификации
        auth_layout = QVBoxLayout()
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Имя пользователя")
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Пароль")
        self.password_input.setEchoMode(QLineEdit.Password)
        
        auth_layout.addWidget(QLabel("Имя пользователя:"))
        auth_layout.addWidget(self.username_input)
        auth_layout.addWidget(QLabel("Пароль:"))
        auth_layout.addWidget(self.password_input)
        
        self.login_btn = QPushButton("Войти")
        self.login_btn.clicked.connect(self.login)
        self.register_btn = QPushButton("Регистрация")
        self.register_btn.clicked.connect(self.register)
        
        auth_layout.addWidget(self.login_btn)
        auth_layout.addWidget(self.register_btn)
        
        left_panel.addLayout(auth_layout)
        
        # Список заметок
        left_panel.addWidget(QLabel("Заметки:"))
        self.notes_list = QListWidget()
        self.notes_list.itemClicked.connect(self.load_note)
        left_panel.addWidget(self.notes_list)
        
        # Кнопки управления заметками
        btn_layout = QHBoxLayout()
        self.refresh_btn = QPushButton("Обновить")
        self.refresh_btn.clicked.connect(self.load_notes)
        self.delete_btn = QPushButton("Удалить")
        self.delete_btn.clicked.connect(self.delete_note)
        
        btn_layout.addWidget(self.refresh_btn)
        btn_layout.addWidget(self.delete_btn)
        left_panel.addLayout(btn_layout)
        
        # Правая панель с редактором заметок
        right_panel = QVBoxLayout()
        
        # Заголовок заметки
        right_panel.addWidget(QLabel("Заголовок:"))
        self.title_input = QLineEdit()
        right_panel.addWidget(self.title_input)
        
        # Содержимое заметки
        right_panel.addWidget(QLabel("Содержимое (Markdown):"))
        self.content_input = QTextEdit()
        self.content_input.setPlaceholderText("Введите текст заметки в формате Markdown...")
        right_panel.addWidget(self.content_input)
        
        # Кнопка сохранения
        self.save_btn = QPushButton("Сохранить заметку")
        self.save_btn.clicked.connect(self.save_note)
        right_panel.addWidget(self.save_btn)
        
        # Создаем splitter для разделения панелей
        splitter = QSplitter(Qt.Horizontal)
        
        # Левая панель
        left_widget = QWidget()
        left_widget.setLayout(left_panel)
        
        # Правая панель
        right_widget = QWidget()
        right_widget.setLayout(right_panel)
        
        splitter.addWidget(left_widget)
        splitter.addWidget(right_widget)
        splitter.setSizes([300, 700])
        
        main_layout.addWidget(splitter)
        
        # Меню
        self.create_menu()
        
        # Статус бар
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Не авторизован")
        
    def create_menu(self):
        menubar = self.menuBar()
        
        # Файл
        file_menu = menubar.addMenu('Файл')
        
        new_action = QAction('Новая заметка', self)
        new_action.triggered.connect(self.new_note)
        file_menu.addAction(new_action)
        
        exit_action = QAction('Выход', self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Помощь
        help_menu = menubar.addMenu('Помощь')
        
        about_action = QAction('О программе', self)
        about_action.triggered.connect(self.about)
        help_menu.addAction(about_action)
    
    def register(self):
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()
        
        if not username or not password:
            QMessageBox.warning(self, "Ошибка", "Введите имя пользователя и пароль")
            return
        
        success, result = self.api.register(username, password)
        if success:
            QMessageBox.information(self, "Успех", f"Пользователь {username} зарегистрирован")
            self.status_bar.showMessage(f"Авторизован как: {username}")
        else:
            QMessageBox.critical(self, "Ошибка", f"Ошибка регистрации: {result}")
    
    def login(self):
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()
        
        if not username or not password:
            QMessageBox.warning(self, "Ошибка", "Введите имя пользователя и пароль")
            return
        
        success, result = self.api.login(username, password)
        if success:
            QMessageBox.information(self, "Успех", f"Добро пожаловать, {username}!")
            self.status_bar.showMessage(f"Авторизован как: {username}")
            self.load_notes()
        else:
            QMessageBox.critical(self, "Ошибка", f"Ошибка входа: {result}")
    
    def load_notes(self):
        if not self.api.user_id:
            QMessageBox.warning(self, "Ошибка", "Сначала войдите в систему")
            return
        
        success, result = self.api.get_notes()
        if success:
            self.notes_list.clear()
            for note in result:
                item_text = f"{note['title']} ({note['updated_at']})"
                self.notes_list.addItem(item_text)
            self.status_bar.showMessage(f"Загружено {len(result)} заметок")
        else:
            QMessageBox.critical(self, "Ошибка", f"Ошибка загрузки заметок: {result}")
    
    def load_note(self, item):
        if not self.api.user_id:
            return
        
        # Получаем индекс выбранного элемента
        index = self.notes_list.currentRow()
        success, notes = self.api.get_notes()
        
        if success and index < len(notes):
            note = notes[index]
            self.current_note_id = note['id']
            self.title_input.setText(note['title'])
            self.content_input.setText(note['content'])
    
    def save_note(self):
        if not self.api.user_id:
            QMessageBox.warning(self, "Ошибка", "Сначала войдите в систему")
            return
        
        title = self.title_input.text().strip()
        content = self.content_input.toPlainText()
        
        if not title:
            title = "Без названия"
        
        if self.current_note_id:
            # Обновляем существующую заметку
            success, result = self.api.update_note(self.current_note_id, title, content)
            if success:
                QMessageBox.information(self, "Успех", "Заметка обновлена")
                self.load_notes()
            else:
                QMessageBox.critical(self, "Ошибка", f"Ошибка обновления: {result}")
        else:
            # Создаем новую заметку
            success, result = self.api.create_note(title, content)
            if success:
                QMessageBox.information(self, "Успех", "Заметка создана")
                self.current_note_id = result['id']
                self.load_notes()
            else:
                QMessageBox.critical(self, "Ошибка", f"Ошибка создания: {result}")
    
    def delete_note(self):
        if not self.current_note_id:
            QMessageBox.warning(self, "Ошибка", "Сначала выберите заметку")
            return
        
        reply = QMessageBox.question(self, "Подтверждение", 
                                   "Вы уверены, что хотите удалить заметку?",
                                   QMessageBox.Yes | QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            success, result = self.api.delete_note(self.current_note_id)
            if success:
                QMessageBox.information(self, "Успех", "Заметка удалена")
                self.current_note_id = None
                self.title_input.clear()
                self.content_input.clear()
                self.load_notes()
            else:
                QMessageBox.critical(self, "Ошибка", f"Ошибка удаления: {result}")
    
    def new_note(self):
        self.current_note_id = None
        self.title_input.clear()
        self.content_input.clear()
    
    def about(self):
        QMessageBox.about(self, "О программе", 
                         "Сервис синхронизированных заметок\n\n"
                         "Возможности:\n"
                         "- Хранение заметок в формате Markdown\n"
                         "- Синхронизация между устройствами\n"
                         "- Аутентификация пользователей\n"
                         "- Создание, редактирование и удаление заметок")

def main():
    app = QApplication(sys.argv)
    window = NotesApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()