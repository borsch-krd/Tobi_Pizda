# API Документация для сервиса синхронизированных заметок

## Базовый URL
`http://localhost:5000/api`

## Аутентификация

### Регистрация пользователя
- **POST** `/api/register`
- Тело запроса:
  ```json
  {
    "username": "string",
    "password": "string"
  }
  ```
- Ответ:
  ```json
  {
    "message": "User registered successfully",
    "user_id": integer
  }
  ```

### Вход пользователя
- **POST** `/api/login`
- Тело запроса:
  ```json
  {
    "username": "string",
    "password": "string"
  }
  ```
- Ответ:
  ```json
  {
    "message": "Login successful",
    "user_id": integer,
    "username": "string"
  }
  ```

## Заметки

### Получить все заметки пользователя
- **GET** `/api/notes?user_id={user_id}`
- Ответ:
  ```json
  {
    "notes": [
      {
        "id": "string",
        "title": "string",
        "content": "string",
        "created_at": "timestamp",
        "updated_at": "timestamp"
      }
    ]
  }
  ```

### Получить конкретную заметку
- **GET** `/api/notes/{note_id}?user_id={user_id}`
- Ответ:
  ```json
  {
    "id": "string",
    "title": "string",
    "content": "string",
    "created_at": "timestamp",
    "updated_at": "timestamp"
  }
  ```

### Создать новую заметку
- **POST** `/api/notes`
- Тело запроса:
  ```json
  {
    "user_id": integer,
    "title": "string",
    "content": "string"
  }
  ```
- Ответ:
  ```json
  {
    "id": "string",
    "title": "string",
    "content": "string",
    "created_at": "timestamp",
    "updated_at": "timestamp"
  }
  ```

### Обновить заметку
- **PUT** `/api/notes/{note_id}`
- Тело запроса:
  ```json
  {
    "user_id": integer,
    "title": "string",
    "content": "string"
  }
  ```
- Ответ:
  ```json
  {
    "id": "string",
    "title": "string",
    "content": "string",
    "updated_at": "timestamp"
  }
  ```

### Удалить заметку
- **DELETE** `/api/notes/{note_id}?user_id={user_id}`
- Ответ:
  ```json
  {
    "message": "Note deleted successfully"
  }
  ```

### Получить заметку в формате HTML
- **GET** `/api/notes/{note_id}/html?user_id={user_id}`
- Ответ:
  ```json
  {
    "id": "string",
    "title": "string",
    "html_content": "rendered html string"
  }
  ```