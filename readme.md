# Портал Букворожка - Система обмена книгами

## Описание

Веб-приложение для обмена книгами между пользователями. Пользователи могут регистрироваться, добавлять свои книги и просматривать книги других пользователей.

## Функционал

- **Регистрация и авторизация** - пользователи могут создавать аккаунты и входить в систему
- **Добавление книг** - пользователи могут добавлять информацию о своих книгах
- **Просмотр каталога** - все пользователи могут видеть доступные книги
- **Личный кабинет** - управление своими книгами
- **Админ панель** - администраторы могут видеть всех пользователей и книги

## Установка и запуск

### 1. Создание виртуального окружения

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# или
venv\Scripts\activate     # Windows
```

### 2. Установка зависимостей

```bash
pip install -r requirements.txt
```

### 3. Структура проекта

Создайте следующую структуру папок:

```
project/
├── app.py
├── requirements.txt
└── templates/
    ├── base.html
    ├── index.html
    ├── register.html
    ├── login.html
    ├── profile.html
    ├── add_book.html
    └── admin.html
```

### 4. Запуск приложения

```bash
python app.py
```

Приложение будет доступно по адресу: http://127.0.0.1:5000

## Использование

### Регистрация

1. Перейдите на страницу регистрации
1. Заполните форму (ФИО, email, телефон, пароль)
1. Нажмите “Зарегистрироваться”

### Добавление книг

1. Войдите в систему
1. Перейдите в “Добавить книгу”
1. Заполните информацию о книге
1. Сохраните

### Создание администратора

Для создания администратора нужно вручную изменить поле `is_admin` в базе данных:

```python
# Запустите Python в папке проекта
from app import app, db, User
with app.app_context():
    user = User.query.filter_by(email='admin@example.com').first()
    user.is_admin = True
    db.session.commit()
```

## Особенности реализации

### База данных

- Используется SQLite для простоты
- Две основные таблицы: User и Book
- Связь один-ко-многим между пользователями и книгами

### Безопасность

- Пароли хешируются с помощью Werkzeug
- Сессии для аутентификации
- Проверка прав доступа

### Интерфейс

- Адаптивный дизайн
- Простая навигация
- Флеш-сообщения для обратной связи

## Возможные улучшения

- Поиск по книгам
- Система запросов на обмен
- Загрузка обложек книг
- Email-уведомления
- Рейтинговая система
- Чат между пользователями
